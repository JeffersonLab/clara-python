#!/usr/bin/env python
#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

import argparse
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgConstants import xMsgConstants

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
from clara.sys.Container import Container
from clara.util.CConstants import CConstants
from clara.util.RequestParser import RequestParser


class DpeCallBack(xMsgCallBack):

    def __init__(self, dpe):
        super(DpeCallBack, self).__init__()
        self.dpe = dpe

    def callback(self, msg):
        try:
            parser = RequestParser.build_from_message(msg)
            cmd = parser.next_string()

            if cmd == CConstants.START_DPE:
                pass

            elif cmd == CConstants.STOP_DPE:
                pass

            elif cmd == CConstants.DPE_PING:
                # Nothing yet
                pass

            elif cmd == CConstants.DPE_UP:
                # Nothing yet
                pass

            elif cmd == CConstants.DPE_DOWN:
                # Nothing yet
                pass

            elif cmd == CConstants.START_CONTAINER:
                xMsgUtil.log("DPE received: " + CConstants.START_CONTAINER)
                self.dpe.run_container(parser.next_string())

            elif cmd == CConstants.STOP_CONTAINER:
                xMsgUtil.log("DPE received: " + CConstants.STOP_CONTAINER)
                self.dpe.stop_container(parser.next_string())

            elif cmd == CConstants.CONTAINER_UP:
                # Nothing yet
                pass

            elif cmd == CConstants.CONTAINER_DOWN:
                # Nothing yet
                pass

            elif cmd == CConstants.START_SERVICE:
                # Nothing yet
                pass

            elif cmd == CConstants.START_SERVICE:
                # Nothing yet
                pass

            else:
                print cmd
                xMsgUtil.log("DPE received: Invalid request...")

        except Exception as e:
            raise e

        finally:
            return msg


class Dpe(ClaraBase):

    fe_host = str(xMsgConstants.UNDEFINED)
    sub_handler = str(xMsgConstants.UNDEFINED)
    my_containers = {}

    def __init__(self, dpe_port, poolsize,
                 registration_host, registration_port,
                 description, cloud_host, cloud_port):
        super(Dpe, self).__init__(ClaraUtils.build_topic(CConstants.DPE,
                                                         "localhost",
                                                         dpe_port),
                                  cloud_host,
                                  registration_host)
        self.print_logo()

        try:
            self.sub_handler = self.listen(self.myname,
                                           self.node_connection,
                                           DpeCallBack(self))
            xMsgUtil.keep_alive()

        except KeyboardInterrupt:
            xMsgUtil.log("Gracefully quitting the dpe...")
            for container in self.my_containers:
                container.stop()
                container.destroy()

            self.unsubscribe(self.sub_handler)
            return

    def print_logo(self):
        print "========================================="
        print "                 CLARA DPE               "
        print "========================================="
        print " Name             = " + self.myname
        print " Date             = " + xMsgUtil.current_time()
        print " Version          = 3.x"
        print "========================================="
        print ""

    def run_container(self, container_name):
        if container_name in self.my_containers:
            xMsgUtil.log("Warning: Container " + str(container_name) +
                         "already exists. No new container is created")
        else:
            name = ClaraUtils.build_topic(self.myname, container_name)
            container = Container(name, "localhost", "localhost")
            self.my_containers[container_name] = container

    def stop_container(self, container_name):
        if container_name in self.my_containers.keys():
            container = self.my_containers.pop(container_name)
            container.stop()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dpe_port", help="Dpe port", type=int,
                        default=int(xMsgConstants.DEFAULT_PORT))
    parser.add_argument("--poolsize", help="Subscription poolsize", type=int,
                        default=2)
    parser.add_argument("--description", help="Description text", type=str,
                        default="Some description...")
    parser.add_argument("--registration_host", help="Registration host",
                        default="localhost")
    parser.add_argument("--registration_port", help="Registration port",
                        type=int, default=int(xMsgConstants.REGISTRAR_PORT))
    parser.add_argument("--cloud_proxy_host", help="Cloud proxy host",
                        default="localhost")
    parser.add_argument("--cloud_proxy_port", help="Cloud proxy port",
                        type=int, default=int(xMsgConstants.DEFAULT_PORT))
    args = parser.parse_args()

    dpe_port = args.dpe_port
    poolsize = args.poolsize

    description = args.description

    registrar_host = args.registration_host
    registrar_port = args.registration_port

    cloud_proxy_host = args.cloud_proxy_host
    cloud_proxy_port = args.cloud_proxy_port

    Dpe(dpe_port, poolsize, registrar_host, registrar_port, description,
        cloud_proxy_host, cloud_proxy_port)


if __name__ == "__main__":
    main()
