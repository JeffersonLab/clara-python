# coding=utf-8

import os

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data.xMsgMeta_pb2 import xMsgMeta
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress

from clara.base.error.ClaraException import ClaraException
from clara.base.ClaraUtils import ClaraUtils
from clara.engine.EngineData import EngineData
from clara.engine.EngineDataType import EngineDataType, Mimetype


class ClaraBase(xMsg):
    """Clara base class providing methods build services, service container
    and orchestrator.
    """
    clara_home = str(xMsgConstants.UNDEFINED)

    def __init__(self,
                 name,
                 proxy_host="localhost",
                 proxy_port=int(xMsgConstants.DEFAULT_PORT),
                 frontend_host="localhost",
                 frontend_port=int(xMsgConstants.DEFAULT_PORT)):

        self._proxy_address = ProxyAddress(proxy_host, proxy_port)
        self._fe_address = ProxyAddress(frontend_host, frontend_port)
        super(ClaraBase, self).__init__(name,
                                        self._proxy_address,
                                        RegAddress(frontend_host,
                                                   frontend_port))

        self.clara_home = os.environ.get('PCLARA_HOME') or ""

    def __repr__(self):
        return str(self.myname)

    def generic_send(self, msg):
        """Sends a text message to another clara actor (message w/topic)

        Sends message using connection from local proxy

        Args:
            msg (xMsgMessage): Message to send
        """
        conn = self.get_connection(self._proxy_address)
        self.publish(conn, msg)

    def get_frontend_address(self):
        """Returns the frontend address

        Returns:
            ProxyAddress
        """
        return self._fe_address

    def listen(self, topic, callback):
        """This method simply calls xMsg subscribe method passing the reference
        to user provided callback method.

        Args:
            topic (xMsgTopic): Topic of subscription
            callback (xMsgCallBack): User provided callback object
        Returns:
            xMsgSubscription
        """
        proxy_address = ProxyAddress(ClaraUtils.get_dpe_host(topic))

        return self.subscribe(proxy_address, topic, callback)

    def stop_listening(self, handle):
        """Stops listening to a subscription

        Args:
            handle (xMsgSubscription): subscription handler object
        """
        self.unsubscribe(handle)

    def send(self, msg):
        """Sends xMsgMessage object to a Clara component

        Args:
            msg (xMsgMessage): xMsg transient message object
        """
        proxy_address = ProxyAddress(ClaraUtils.get_dpe_host(msg.topic),
                                     ClaraUtils.get_dpe_port(msg.topic))
        conn = self.get_connection(proxy_address)
        self.publish(conn, msg)

    def send_frontend(self, msg):
        """Sends xMsgMessage object to the Frontend

        Args:
            msg (xMsgMessage): xMsg transient message object
        """
        conn = self.get_connection(self._fe_address)
        self.publish(conn, msg)

    def send_response(self, msg, status, data):
        """Sends response to sender

        Args:
            msg (xMsgMessage): received from sender
            status (xMsgMeta.Status): status of the request
            data (String): attached data with the response
        """
        try:
            r_msg = xMsgMessage.create_with_string(msg.get_reply_topic(), data)
            r_msg.metadata.author = self.myname
            r_msg.metadata.status = status
            self.generic_send(r_msg)
        except Exception as e:
            print e.message

    def sync_send(self, msg, timeout):
        """Sends xMsgMessage object to an xMsg actor synchronously

        Args:
            msg (xMsgMessage): xMsg transient message object
            timeout (int): response message timeout in seconds
        """
        proxy_address = ProxyAddress(ClaraUtils.get_dpe_host(msg.topic),
                                     ClaraUtils.get_dpe_port(msg.topic))
        conn = self.get_connection(proxy_address)
        self.sync_publish(conn, msg, timeout)

    def register(self, topic, description=None):
        """Registers the clara actor into the cloud registrar

        Args:
            topic (xMsgTopic): topic to be suscribed
            description (str): description of the actor
        """
        self.register_as_subscriber(self.default_registrar_address,
                                    topic,
                                    description)

    def remove_registration(self, topic):
        """Removes actor's registration from the given topic

        Args:
            topic (xMsgTopic): topic which actor will stop receiving
        """
        self.remove_as_subscriber(topic)

    def discover(self, topic):
        """Discover other clara actors publishing the given topic
        Args:
            topic (xMsgTopic): topic to discover in the cloud
        Returns:
            Set
        """
        return self.find_subscriber(topic)

    def serialize(self, topic, engine_data, datatypes):
        """Builds a message by serializing passed data object using
        serialization routine defined in one of the data types objects

        Args:
             topic (xMsgTopic): the topic where data will be published
             engine_data (EngineData): the data to be serialized
             datatypes (set(<EngineDataType>)): the set of registered dataTypes

        Returns:
            xMsgMessage: Message with serialized data
        """
        assert isinstance(engine_data, EngineData)
        for dt in datatypes:
            if dt.mimetype == engine_data.mimetype:
                msg = xMsgMessage()
                msg.topic = str(topic)
                msg.metadata = engine_data.metadata
                msg.data = dt.serializer.write(engine_data.get_data())
                return msg

        if engine_data.mimetype == Mimetype.STRING:
            msg = xMsgMessage()
            msg.topic = str(topic)
            msg.metadata = engine_data.metadata
            msg.data = EngineDataType.STRING().serializer.write(engine_data.get_data())
            return msg

    def de_serialize(self, msg, datatypes):
        """ De serializes data of the message, represented as bytes into an
        object of az type defined using the mimetype/datatype of the metadata

        Args:
            msg (xMsgMessage): message to be deserialized
            datatypes (set(<EngineDataType>): datatype set of permitted
                serializations

        Returns:
            EngineData:
        """
        assert isinstance(msg, xMsgMessage)
        for dt in datatypes:
            if dt.mimetype == msg.metadata.dataType:
                try:
                    engine_data = EngineData()
                    engine_data.metadata = msg.metadata
                    engine_data.set_data(msg.metadata.dataType,
                                         dt.serializer.read(msg.data))
                    return engine_data

                except Exception as e:
                    raise ClaraException("Clara-Error: Could not serialize. %s"
                                         % e.message)
        if msg.metadata.dataType == Mimetype.STRING:
            engine_data = EngineData()
            engine_data.metadata = msg.metadata
            engine_data.set_data(Mimetype.STRING,
                                 EngineDataType.STRING().serializer.read(msg.data))
            return engine_data

        raise ClaraException("Clara-Error: Unsopported mimetype = %s"
                             % msg.metadata.dataType)

    def build_system_error_data(self, msg, severity, description):
        """Builds an EngineData object for error reporting

        Args:
            msg (xMsgMessage): message received
            severity (int): severity of the error
            description (str): description of the error

        Returns:
            EngineData
        """
        out_data = EngineData()
        out_data.set_data(Mimetype.STRING, msg)
        out_data.description = description
        out_data.status = xMsgMeta.ERROR
        out_data.severity = severity

        return out_data
