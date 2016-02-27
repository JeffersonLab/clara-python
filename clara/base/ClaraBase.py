# coding=utf-8
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
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress


class ClaraBase(xMsg):
    """Base class for service and orchestrator classes as well

    Clara service name convention - dpe-host_lang:container:engine_name
    """
    sub_handler = str(xMsgConstants.UNDEFINED)
    node_connection = str(xMsgConstants.UNDEFINED)
    clara_home = str(xMsgConstants.UNDEFINED)


    def __init__(self, name, proxy_host, frontend_host, proxy_port, frontend_port):
        proxy_address = ProxyAddress(host=proxy_host, pub_port=proxy_port)
        fe_address = RegAddress(host=frontend_host, port=frontend_port)
        super(ClaraBase, self).__init__(name, proxy_address, fe_address)

        # Create a socket connections to the xMsg node
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
        """Stops listening to a subscription defined by the handler

        handle (xMsgSubscription): subscription handler object

        """
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
            timeout (int): response message timeout in seconds
        """
        self.sync_publish(self.node_connection, msg, timeout)

    def register(self, topic, description=None):
        self.register_as_subscriber(self.default_registrar_address, topic,
                                    description)

    def remove_registration(self, topic):
        self.remove_as_subscriber(topic)

    def discover(self, topic):
        return self.find_subscriber(topic)
