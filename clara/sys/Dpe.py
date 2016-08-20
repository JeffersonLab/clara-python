#!/usr/bin/env python
# coding=utf-8

from getpass import getuser

from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgConstants import xMsgConstants

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

    my_containers = dict()
    subscription_handler = None

    def __init__(self,
                 proxy_host="localhost",
                 frontend_host="localhost",
                 proxy_port=int(xMsgConstants.DEFAULT_PORT),
                 frontend_port=int(xMsgConstants.DEFAULT_PORT)):

        if proxy_host == frontend_host:
            proxy_host = xMsgUtil.host_to_ip(proxy_host)
            frontend_host = proxy_host
        else:
            proxy_host = xMsgUtil.host_to_ip(proxy_host)
            frontend_host = xMsgUtil.host_to_ip(frontend_host)

        dpe_name = DpeName(str(proxy_host), proxy_port, ClaraLang.PYTHON)

        super(Dpe, self).__init__(dpe_name.canonical_name(),
                                  proxy_host,
                                  proxy_port,
                                  frontend_host,
                                  frontend_port)
        self._is_frontend = True if frontend_host == proxy_host else False
        self.dpe_name = dpe_name
        self._logger = ClaraLogger(repr(self))
        self._print_logo()
        self._report = DpeReport(self, getuser())

        topic = ClaraUtils.build_topic(CConstants.DPE, self.myname)
        self.subscription_handler = None

        try:
            self.subscription_handler = self.listen(topic, _DpeCallBack(self))
            xMsgUtil.keep_alive()

        except KeyboardInterrupt:
            self._exit()

        finally:
            self.stop_listening(self.subscription_handler)

    def __repr__(self):
        return str("Dpe:%s" % self.myname)

    def _exit(self):
        self._logger.log_info("Gracefully quitting the dpe...")
        for container in self.my_containers.itervalues():
            container.exit()
            container.destroy()

    def _print_logo(self):
        import platform
        print "=" * 80
        print " " * 35 + "CLARA DPE"
        print "=" * 80
        print ""
        print " Name             = " + self.myname
        print " Date             = " + xMsgUtil.current_time()
        print " Version          = " + platform.python_version()
        print " Binding          = Python"
        print ""
        print " Proxy Host       = %s" % self._proxy_address.host
        print " Proxy Port       = %d" % self._proxy_address.pub_port
        print ""
        if not self._is_frontend:
            print " Frontend Host    = %s" % self._fe_address.host
            print " Frontend Port    = %d" % self._fe_address.pub_port
            print ""
        print "=" * 80
        print ""

    def start_container(self, parser):
        container_name = parser.next_string()
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

    def stop_container(self, parser):
        container_name = parser.next_string()
        if container_name in self.my_containers:
            container = self.my_containers.pop(container_name)
            self._report.remove_container(container.get_report())
            container.exit()

    def start_service(self, parser):
        try:
            service_name = parser.next_string()
            container_name = ClaraUtils.get_container_name(service_name)
            engine_name = parser.next_string()
            engine_class = parser.next_string()
            pool_size = parser.next_integer()
            description = parser.next_string()
            initial_state = parser.next_string()

            if container_name in self.my_containers:
                self.my_containers[container_name].add_service(engine_name,
                                                               engine_class,
                                                               pool_size,
                                                               initial_state)

        except Exception as e:
            self._logger.log_exception(e.message)
            raise e

    def stop_service(self, parser):
        container_name = parser.next_string()
        engine_name = parser.next_string()
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


class _DpeCallBack(xMsgCallBack):

    def __init__(self, dpe):
        super(_DpeCallBack, self).__init__()
        self._dpe = dpe
        self._logger = ClaraLogger(repr(dpe))

    def callback(self, msg):
        try:
            parser = RequestParser.build_from_message(msg)
            cmd = parser.next_string()
            self._logger.log_info("received: %s" % cmd)

            if cmd == CConstants.STOP_DPE:
                self._dpe.exit()

            elif cmd == CConstants.START_CONTAINER:
                self._dpe.start_container(parser)

            elif cmd == CConstants.STOP_CONTAINER:
                self._dpe.stop_container(parser)

            elif cmd == CConstants.START_SERVICE:
                self._dpe.start_service(parser)

            elif cmd == CConstants.STOP_SERVICE:
                self._dpe.stop_service(parser)

        except Exception as e:
            self._logger.log_exception(e.message)
            raise e

        finally:
            return msg


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--fe_host", help="Frontend address", type=str,
                        default="localhost")
    parser.add_argument("--fe_port", help="Frontend port", type=int,
                        default=7771)
    parser.add_argument("--dpe_port", help="Local port", type=int,
                        default=7771)

    args = parser.parse_args()
    frontend_host = args.fe_host
    frontend_port = args.fe_port
    local_port = args.dpe_port

    Dpe("localhost", frontend_host, local_port, frontend_port)


if __name__ == "__main__":
    main()
