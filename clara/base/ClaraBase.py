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

import os
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.net.xMsgAddress import RegAddress, ProxyAddress

from clara.base.ClaraUtils import ClaraUtils
from clara.base.error.ClaraException import ClaraException
from clara.util.CConstants import CConstants


class ClaraBase(xMsg):
    """Base class for service and orchestrator classes as well

    Clara service name convention - dpe-host_lang:container:engine_name
    """
    node_connection = str(xMsgConstants.UNDEFINED)
    clara_home = str(xMsgConstants.UNDEFINED)
    frontend = str(xMsgConstants.UNDEFINED)

    def __init__(self, name, frontend, proxy_address, reg_address="localhost"):
        super(ClaraBase, self).__init__(name,
                                        ProxyAddress(proxy_address),
                                        RegAddress(reg_address))

        # Create a socket connections to the xMsg node
        self.frontend = frontend
        self.clara_home = os.environ.get('PCLARA_HOME')
        self.node_connection = self.connect()

    def listen(self, topic, connection, callback):
        """This method simply calls xMsg subscribe method passing the reference to
        user provided callback method.

        Args:
            topic (xMsgTopic): Topic of subscription
            callback (xMsgCallBack): User provided callc_back object
        """
        return self.subscribe(topic, connection, callback)

    def stop_listening(self, handle):
        self.unsubscribe(handle)

    def send(self, msg):
        """Sends xMsgMessage object to a Clara component

        Args:
            msg (xMsgMessage): xMsg transient message object
        """
        self.publish(self.node_connection, msg)

    def sync_send(self, msg, timeout):
        """Sends xMsgMessage object to an xMsg actor synchronously

        Args:
            msg (xMsgMessage): xMsg transient message object
        """
        self.sync_publish(self.node_connection, msg, timeout)

    def serialize(self, data, message, datatypes):
        """Builds a message by serializing passed data
        """
        pass

    def de_serialize(self, message, datatypes):
        pass

    def register(self, topic, description):
        pass

    def __deploy(self, clara_component, timeout):
        if ClaraUtils.is_container_name(clara_component):
            args = [CConstants.START_CONTAINER] + \
                ClaraUtils.decompose_canonical_name(clara_component)
            data = ClaraUtils.build_data(args)

        elif ClaraUtils.is_service_name(clara_component):
            args = [CConstants.START_SERVICE] + \
                ClaraUtils.decompose_canonical_name(clara_component)
            data = ClaraUtils.build_data(args)

        else:
            raise ClaraException("Unknown or undefined component type.")

        msg = self.__create_request(clara_component, data)
        return msg

    def __send(self, clara_component, msg, timeout=0):
        if timeout > 0:
            return self.sync_send(msg, timeout)
        else:
            self.send(msg)

    def __exit(self, clara_component, timeout):
        topic = ClaraUtils.build_topic(CConstants.DPE,
                                       ClaraUtils.get_dpe_name(clara_component))
        if ClaraUtils.is_dpe_name(clara_component):
            data = CConstants.STOP_DPE
        elif ClaraUtils.is_container_name(clara_component):
            data = ClaraUtils.build_data(CConstants.STOP_SERVICE,
                                         ClaraUtils.get_container_name(clara_component),
                                         ClaraUtils.get_engine_name(clara_component))
            msg = self.__create_request(topic, data)
            return msg

    def report_FE(self, command):
        topic = xMsgTopic.wrap(CConstants.DPE + " " + self.myname)

    def __create_request(self, topic, data):
        msg = xMsgMessage()
        msg.set_topic(topic)
        msg.set_data(str(data), str(xMsgConstants.STRING))
