# coding=utf-8

import os

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data.xMsgMeta_pb2 import xMsgMeta
from xmsg.net.xMsgAddress import ProxyAddress, RegAddress

from clara.base.error.ClaraException import ClaraException
from clara.engine.EngineData import EngineData
from clara.engine.EngineDataType import EngineDataType, Mimetype


class ClaraBase(xMsg):
    """Base class for service and orchestrator classes as well

    Clara service name convention - dpe-host_lang:container:engine_name
    """
    sub_handler = str(xMsgConstants.UNDEFINED)
    clara_home = str(xMsgConstants.UNDEFINED)
    _node_connection = str(xMsgConstants.UNDEFINED)

    def __init__(self, name, proxy_host, frontend_host, proxy_port,
                 frontend_port):
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
            callback (xMsgCallBack): User provided callback object
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

    def send_frontend(self, msg):
        # TODO: Placeholder for now, needs to refactor frontend connections
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
                    user_data = dt.serializer.read(msg.data)
                    engine_data = EngineData()
                    engine_data.metadata = msg.metadata
                    engine_data.set_data(msg.metadata.dataType, user_data)
                    return engine_data

                except Exception as e:
                    raise ClaraException("Clara-Error: Could not serialize. %s"
                                         % e.message)
        raise ClaraException("Clara-Error: Unsopported mimetype = %s"
                             % msg.metadata.dataType)

    def build_system_error_data(self, msg, severity, description):
        out_data = EngineData()
        out_data.set_data(Mimetype.STRING, msg)
        out_data.description = description
        out_data.status = xMsgMeta.ERROR
        out_data.severity = severity

        return out_data
