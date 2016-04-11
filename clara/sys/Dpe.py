#!/usr/bin/env python
# coding=utf-8

import argparse
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraLang import ClaraLang
from clara.base.ClaraNames import DpeName, ContainerName
from clara.base.ClaraUtils import ClaraUtils
from clara.sys.Container import Container
from clara.util.CConstants import CConstants
from clara.util.ClaraLogger import ClaraLogger
from clara.util.RequestParser import RequestParser


class Dpe(ClaraBase):

    my_containers = dict()
    subscription_handler = None

    def __init__(self, local_address, frontend_address,
                 proxy_port=int(xMsgConstants.DEFAULT_PORT),
                 frontend_port=int(xMsgConstants.REGISTRAR_PORT)):
        dpe_name = DpeName(xMsgUtil.host_to_ip(local_address),
                           proxy_port, ClaraLang.PYTHON)

        super(Dpe, self).__init__(dpe_name.canonical_name(),
                                  local_address,
                                  frontend_address,
                                  proxy_port,
                                  frontend_port)
        self.dpe_name = dpe_name
        self.logger = ClaraLogger(repr(self))
        self.print_logo()

        topic = ClaraUtils.build_topic(CConstants.DPE, self.myname)
        try:
            self.subscription_handler = self.listen(topic, _DpeCallBack(self))
            xMsgUtil.keep_alive()

        except KeyboardInterrupt:
            self.exit()

    def __repr__(self):
        return str("Dpe:%s" % self.myname)

    def exit(self):
        self.logger.log_info("Gracefully quitting the dpe...")
        for container in self.my_containers:
            container.exit()
            container.destroy()
        self.stop_listening(self.subscription_handler)

    def print_logo(self):
        print "================================================"
        print "                 CLARA DPE"
        print "================================================"
        print " Name             = " + self.myname
        print " Date             = " + xMsgUtil.current_time()
        print " Version          = 2.x"
        print " Lang             = Python 2.7.11"
        print ""
        print " Proxy Host       = %s" % self.default_proxy_address.host
        print " Proxy Port       = %d" % self.default_proxy_address.pub_port
        print ""
        print " Frontend Host    = %s" % self.default_registrar_address.host
        print " Frontend Post    = %d" % self.default_registrar_address.port
        print ""
        print "================================================"
        print ""

    def start_container(self, parser):
        container_name = parser.next_string()
        try:
            if container_name in self.my_containers:
                self.logger.log_warning("Container " + str(container_name) +
                                        " already exists. No new container is"
                                        " created")
            else:
                container = Container(ContainerName(self.dpe_name,
                                                    container_name),
                                      ProxyAddress(), RegAddress())
                self.my_containers[container_name] = container

        except Exception as e:
            self.logger.log_exception(e.message)
            raise e

    def stop_container(self, parser):
        container_name = parser.next_string()
        if container_name in self.my_containers:
            container = self.my_containers.pop(container_name)
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
            self.logger.log_exception(e.message)
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
        self.dpe = dpe

    def callback(self, msg):
        try:
            parser = RequestParser.build_from_message(msg)
            cmd = parser.next_string()
            self.dpe.logger.log_info("received: %s" % cmd)

            if cmd == CConstants.STOP_DPE:
                self.dpe.exit()

            elif cmd == CConstants.START_CONTAINER:
                self.dpe.start_container(parser)

            elif cmd == CConstants.STOP_CONTAINER:
                self.dpe.stop_container(parser)

            elif cmd == CConstants.START_SERVICE:
                self.dpe.start_service(parser)

            elif cmd == CConstants.STOP_SERVICE:
                self.dpe.stop_service(parser)

        except Exception as e:
            raise e

        finally:
            return msg


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--fe_host", help="Frontend address", type=str,
                        default="localhost")
    parser.add_argument("--fe_port", help="Frontend port", type=int,
                        default=8888)
    parser.add_argument("--dpe_port", help="Local dpe address", type=int,
                        default=7771)

    args = parser.parse_args()
    frontend_address = args.fe_host
    frontend_port = args.fe_port
    local_port = args.dpe_port

    Dpe("localhost", frontend_address, local_port, frontend_port)


if __name__ == "__main__":
    main()
