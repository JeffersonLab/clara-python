# coding=utf-8

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
    clara_home = str(xMsgConstants.UNDEFINED)
    _node_connection = str(xMsgConstants.UNDEFINED)

    def __init__(self, name, proxy_host, frontend_host, proxy_port, frontend_port):
        proxy_address = ProxyAddress(host=proxy_host, pub_port=proxy_port)
        fe_address = RegAddress(host=frontend_host, port=frontend_port)
        super(ClaraBase, self).__init__(name, proxy_address, fe_address)

        # Create a socket connections to the xMsg node
        self.clara_home = os.environ.get('PCLARA_HOME')
        self._node_connection = self.connect()

    def listen(self, topic, callback):
        """This method simply calls xMsg subscribe method passing the reference
        to user provided callback method.

        Args:
            topic (xMsgTopic): Topic of subscription
            callback (xMsgCallBack): User provided callc_back object
        """
        return self.subscribe(topic, self._node_connection, callback)

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
        self.publish(self._node_connection, msg)

    def sync_send(self, msg, timeout):
        """Sends xMsgMessage object to an xMsg actor synchronously

        Args:
            msg (xMsgMessage): xMsg transient message object
            timeout (int): response message timeout in seconds
        """
        self.sync_publish(self._node_connection, msg, timeout)

    def register(self, topic, description=None):
        self.register_as_subscriber(self.default_registrar_address, topic,
                                    description)

    def remove_registration(self, topic):
        self.remove_as_subscriber(topic)

    def discover(self, topic):
        return self.find_subscriber(topic)
