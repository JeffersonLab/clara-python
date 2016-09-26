#!/usr/bin/env python
# coding=utf-8

from multiprocessing import Queue
from multiprocessing.queues import Empty
from threading import Thread, Event
from getpass import getuser

import os
import signal
import subprocess

from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.data.xMsgMeta_pb2 import xMsgMeta

from clara import __version__ as clara_version
from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraLang import ClaraLang
from clara.base.ClaraNames import DpeName, ContainerName
from clara.base.ClaraUtils import ClaraUtils
from clara.sys.Container import Container
from clara.util.CConstants import CConstants
from clara.util.ClaraLogger import ClaraLogger
from clara.util.reports.DpeReport import DpeReport
from clara.util.RequestParser import RequestParser


class Dpe(ClaraBase):
    """Clara data processing environment. It can play the role of the Front-End
    (FE), which is the static point of the entire cloud. It creates and manages
    the registration database (local and case of being assigned as an FE: global
    database). Note this is a copy of the subscribers database resident in the
    xMsg registration database. This also creates a shared memory for
    communicating Clara transient data objects between services within the same
    process (this avoids data serialization and de-serialization).
    """

    my_containers = dict()
    subscription_handler = None

    def __init__(self, proxy_host, frontend_host, proxy_port, frontend_port,
                 report_interval=5):
        """Dpe Constructor

        Args:
            proxy_host (String): local hostname
            frontend_host (String): frontend hostname
            proxy_port (int): proxy port, default is 7791
            frontend_port (int): frontend port, default is 7791
            report_interval (int): time interval in seconds for reporting
                service to update the frontend

        Returns:
            Dpe: Dpe object
        """
        if proxy_host == frontend_host and proxy_host == frontend_port:
            proxy_host = xMsgUtil.host_to_ip(proxy_host)
            frontend_host = proxy_host
            _is_frontend = True
        else:
            proxy_host = xMsgUtil.host_to_ip(proxy_host)
            frontend_host = xMsgUtil.host_to_ip(frontend_host)
            _is_frontend = False

        dpe_name = DpeName(str(proxy_host), proxy_port, ClaraLang.PYTHON)

        super(Dpe, self).__init__(dpe_name.canonical_name(),
                                  proxy_host,
                                  proxy_port,
                                  frontend_host,
                                  frontend_port)
        self.dpe_name = dpe_name
        self._is_frontend = _is_frontend
        self._logger = ClaraLogger(repr(self))
        self._print_logo()

        if not self._is_frontend:
            self._report = DpeReport(self, getuser())
            self._report_control = Event()
            self._report_service = _ReportingService(self._report_control,
                                                     report_interval, self)
            self._report_service.start()

        self.subscription_handler = None
        self._start()

    def _exit(self):
        self._report_control.set()
        self._logger.log_info("Gracefully quitting the dpe...")
        for container in self.my_containers.itervalues():
            container.exit()
            container.destroy()

    def _print_logo(self):
        import platform
        logo_width = 50
        print "=" * logo_width
        print " " * 20 + "CLARA DPE"
        print "=" * logo_width
        print ""
        print " Name             = %s" % self.myname
        print " Date             = %s" % xMsgUtil.current_time()
        print " Version          = %s" % clara_version
        print " Lang             = python-%s" % platform.python_version()
        print ""
        print " Proxy Host       = %s" % self._proxy_address.host
        print " Proxy Port       = %d" % self._proxy_address.pub_port
        print ""
        if not self._is_frontend:
            print " Frontend Host    = %s" % self._fe_address.host
            print " Frontend Port    = %d" % self._fe_address.pub_port
            print ""
        print "=" * logo_width
        print ""

    def _start(self):
        proxy_process = subprocess.Popen(['px_proxy'])

        try:
            topic = ClaraUtils.build_topic(CConstants.DPE, self.myname)
            task_queue = Queue()
            self.subscription_handler = self.listen(topic,
                                                    _DpeCallBack(task_queue))

            def _interruptible_get():
                try:
                    return task_queue.get_nowait()
                except Empty:
                    return None

            while True:
                s_msg = _interruptible_get()
                if s_msg:
                    msg = xMsgMessage.from_serialized_data(s_msg)
                    self._process_request(msg)

        except KeyboardInterrupt:
            print "Ctrl-C"
            self._exit()
            self.stop_listening(self.subscription_handler)
            os.kill(proxy_process.pid, signal.SIGINT)

    def _process_request(self, request):
        parser = RequestParser.build_from_message(request)
        cmd = parser.next_string()
        response = parser.request()

        self._logger.log_info("received: %s" % cmd)

        if cmd == CConstants.START_CONTAINER:
            self.start_container(parser)

        elif cmd == CConstants.STOP_CONTAINER:
            self.stop_container(parser)

        elif cmd == CConstants.START_SERVICE:
            self.start_service(parser)

        elif cmd == CConstants.STOP_SERVICE:
            self.stop_service(parser)

        else:
            print "Unknown DPE request..."

        if request.has_reply_topic():
            self.send_response(request, xMsgMeta.INFO, response)

    def get_report(self):
        """Returns DPE report object

        Returns:
            DpeReport
        """
        return self._report

    def start_container(self, request):
        """Starts a Clara container.

        Containers are required in order to launch a Clara service

        Args:
            request (RequestParser): Request received from Orchestrator to
                create a Container
        """
        container_name = request.next_string()
        try:
            if container_name in self.my_containers:
                self._logger.log_warning("Container " + str(container_name) +
                                         " already exists. No new container is"
                                         " created")
            else:
                container = Container(ContainerName(self.dpe_name,
                                                    container_name),
                                      self._proxy_address,
                                      self._fe_address)
                self.my_containers[container_name] = container
                self._report.add_container(container.get_report())

        except Exception as e:
            self._logger.log_exception(e.message)
            raise e

    def stop_container(self, request):
        """Removes a Clara container and its contained services

        Args:
            request (RequestParser): Request received from Orchestrator to
                stop a Container
        """
        container_name = request.next_string()
        if container_name in self.my_containers:
            container = self.my_containers.pop(container_name)
            self._report.remove_container(container.get_report())
            container.exit()

    def start_service(self, request):
        """Starts a Clara service

        Args:
            request (RequestParser): Request received from Orchestrator to
                start a Service
        """
        try:
            container_name = request.next_string()
            engine_name = request.next_string()
            engine_class = request.next_string()
            pool_size = request.next_integer()
            description = request.next_string()
            initial_state = request.next_string()

            if container_name in self.my_containers:
                self.my_containers[container_name].add_service(engine_name,
                                                               engine_class,
                                                               pool_size,
                                                               initial_state)

        except Exception as e:
            self._logger.log_exception(e.message)
            raise e

    def stop_service(self, request):
        """Stops a running Clara service

        Args:
            request (RequestParser): Request received from Orchestrator to
                stop a Service
        """
        container_name = request.next_string()
        engine_name = request.next_string()
        service_name = ClaraUtils.form_service_name(container_name,
                                                    engine_name)
        if container_name in self.my_containers:
            try:
                self.my_containers[container_name].remove_service(service_name)

            except Exception as e:
                raise Exception("Could not stop service %s: %s "
                                % (service_name, e))

        else:
            raise Exception("Could not stop service %s: missing container "
                            % service_name)


class _ReportingService(Thread):
    """DPE Reporting service

    Service in charge of reporting Runtime time and Registration data to the
    Frontend DPE. The user defines the time interval between updates, default
    is 5.
    """
    def __init__(self, event, interval, base):
        """
        Args:
            event (threading.Event): Event object for thread controlling, kill
                the thread properly.
            interval (int): time interval in seconds for updating the frontend
            base (ClaraBase): ClaraBase object
        """
        Thread.__init__(self)
        self._stopped = event
        self._interval = interval
        self._base = base

    def run(self):
        from xmsg.core.xMsgMessage import xMsgMessage
        while not self._stopped.wait(self._interval):
            report = self._base.get_report().to_json()
            report_alive = self._base.get_report().get_alive_data()
            self._base.send_frontend(
                xMsgMessage.from_string(CConstants.DPE_ALIVE, report_alive))
            self._base.send_frontend(
                xMsgMessage.from_string(CConstants.DPE_REPORT, report))


class _DpeCallBack(xMsgCallBack):

    def __init__(self, q):
        super(_DpeCallBack, self).__init__()
        self._queue = q

    def callback(self, msg):
        self._queue.put(msg.serialize())



def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--fe_host", help="Frontend address", type=str,
                        default="localhost")
    parser.add_argument("--fe-port", help="Frontend port", type=int,
                        default=xMsgConstants.DEFAULT_PORT)
    parser.add_argument("--dpe-port", help="Local port", type=int,
                        default=xMsgConstants.DEFAULT_PORT)
    parser.add_argument("--report-interval", help="Reporting interval",
                        type=int, default=5)

    args = parser.parse_args()
    frontend_host = args.fe_host
    frontend_port = args.fe_port
    local_port = args.dpe_port
    report_interval = args.report_interval

    Dpe("localhost", frontend_host, local_port, frontend_port, report_interval)


if __name__ == "__main__":
    main()
