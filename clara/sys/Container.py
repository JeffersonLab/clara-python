#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
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

from xmsg.core.xMsgCallBack import xMsgCallBack
from xmsg.core.xMsgUtil import xMsgUtil

from clara.base.ClaraBase import ClaraBase
from clara.util.CConstants import CConstants
from clara.util.RequestParser import RequestParser
from xmsg.core.xMsgConstants import xMsgConstants


class ContainerCallBack(xMsgCallBack):

    def __init__(self, container):
        super(ContainerCallBack, self).__init__()
        self.container = container

    def callback(self, msg):
        parser = RequestParser.build_from_message(msg)
        cmd = parser.next_string()

        if cmd == CConstants.DEPLOY_SERVICE:
            xMsgUtil.log("Container received: " + CConstants.DEPLOY_SERVICE)

        elif cmd == CConstants.REMOVE_CONTAINER:
            xMsgUtil.log("Container received: " + CConstants.REMOVE_CONTAINER)

        elif cmd == CConstants.REMOVE_SERVICE:
            xMsgUtil.log("Container received: " + CConstants.REMOVE_SERVICE)

        else:
            xMsgUtil.log("Container: Invalid request...")


class Container(ClaraBase):
    my_services = {}
    subscription_handler = str(xMsgConstants.UNDEFINED)

    def __init__(self, name, local_address, frontend_address):
        super(Container, self).__init__(name,
                                        local_address,
                                        frontend_address)

        self.my_services = set()
        xMsgUtil.log("Container started: " + self.myname)

        self.subscription_handler = self.listen(self.myname,
                                                self.node_connection,
                                                ContainerCallBack(self))

    def add_service(self, engine_name, engine_class_path, service_pool_size,
                    initial_state):
        # TODO: Service constructor
        pass

    def remove_service(self, service_name):
        if service_name in self.my_services:
            service = self.my_services.remove(service_name)
            service.exit()

    def stop(self):
        self.stop_listening(self.subscription_handler)
        self.subscription_handler = None
        xMsgUtil.log("Container stopped: " + self.myname)
