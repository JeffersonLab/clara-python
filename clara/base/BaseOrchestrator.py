# coding=utf-8

import random

from xmsg.core.xMsgExceptions import MalformedCanonicalName
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.data.xMsgMeta_pb2 import xMsgMeta

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
from clara.engine.EngineDataType import EngineDataType, Mimetype
from clara.util.CConstants import CConstants
from clara.util.report.ReportType import ReportType


class BaseOrchestrator(object):
    base = CConstants.UNDEFINED
    name = CConstants.UNDEFINED

    def __init__(self, fe_host="localhost", pool_size=2):
        self.fe_host = fe_host
        self.pool_size = pool_size
        self.name = BaseOrchestrator._generate_name()
        self.base = self._get_clara_base()
        self.datatypes = set()
        self.subscription = dict()

    @staticmethod
    def _generate_name():
        return "orchestrator_%d" % (random.randint(0, 1000))

    def _get_clara_base(self):
        localhost = ClaraUtils.localhost()
        return ClaraBase(self.name, localhost, localhost,
                         int(xMsgConstants.DEFAULT_PORT),
                         int(xMsgConstants.REGISTRAR_PORT))

    @staticmethod
    def _create_request(topic, data, metadata=None):
        msg = xMsgMessage(topic=topic)
        msg.data = data

        if metadata:
            msg.metadata = metadata
        else:
            msg.mimetype = Mimetype.STRING
        return msg

    def exit_dpe(self, dpe_name):
        """Sends message to DPE and requesting to stop

        Args:
            dpe_name (String): name of the dpe to stop
        """
        if not ClaraUtils.is_dpe_name(dpe_name):
            raise MalformedCanonicalName("Malformed DPE name: %s" % dpe_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        self.base.send(xMsgMessage(topic, CConstants.DPE_EXIT))

    def exit_container(self, container_name):
        """Sends message to Container and requesting to stop

        Args:
            container_name (String): name of the container to stop
        """
        if not ClaraUtils.is_container_name(container_name):
            raise ValueError("Bad Container name")

        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe)
        data = ClaraUtils.build_data(CConstants.STOP_CONTAINER, name)

        self.base.send(self._create_request(topic, data))

    def deploy_container(self, container_name, pool_size=2,
                         description="Undefined"):
        """ Sends request to DPE to deploy given container

        Args:
            container_name (String): container name in canonical form
            pool_size (int): pool size for the given container
            description (String): short description for the container
        """
        if not ClaraUtils.is_container_name(container_name):
            raise ValueError("Bad Container name")

        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe)
        data = ClaraUtils.build_data(CConstants.START_CONTAINER,
                                     name, pool_size, description)

        self.base.send(self._create_request(topic, data))

    def register_datatype(self, datatype):
        """Register a single EngineDataType

        Adds this EngineDataType to the datatypes set

        Args:
            datatype (EngineDataType): Engine data type to register
        """
        assert isinstance(datatype, EngineDataType)
        self.datatypes.add(datatype)

    def register_datatypes(self, datatypes):
        """Register the necessary data-types to communicate data to services

        EngineDataType contains user provided data serialization routine

        Args:
            datatypes (set(<EngineDataTypes>): set of data-type objects
        """
        assert isinstance(datatypes, set)
        for d_type in datatypes:
            assert isinstance(d_type, EngineDataType)
        self.datatypes.union(datatypes)

    def configure_service_data_reporting_start(self, service_name,
                                               event_count):
        topic = ClaraUtils.build_topic(CConstants.SERVICE, service_name)
        data = ClaraUtils.build_data(ReportType.DATA, str(event_count))
        msg = self._create_request(topic, data)
        self.base.send(msg)

    def configure_service_data_reporting_stop(self, service_name):
        pass

    def configure_service_done_reporting_start(self, service_name,
                                               event_count):
        topic = ClaraUtils.build_topic(CConstants.SERVICE, service_name)
        data = ClaraUtils.build_data(ReportType.DONE, str(event_count))
        self.base.send(self._create_request(topic, data))

    def configure_service_done_reporting_stop(self, service_name):
        pass

    def configure_service(self, service_name, config_data):
        """Sends configuration request to specified clara service

        Args:
            service_name (String): service name in canonical form
            config_data (EngineData): configuration data
        """
        topic = ClaraUtils.build_topic(CConstants.SERVICE, service_name)

        config_data.metadata.action = xMsgMeta.CONFIGURE

        msg = self.base.serialize(topic, config_data, self.datatypes)
        self.base.send(msg)

    def deploy_service(self, service_name, class_path, pool_size=1,
                       description=CConstants.UNDEFINED,
                       initial_state=CConstants.UNDEFINED):
        """Sends request to DPE to deploy given service

        Args:
            service_name (String): service name in canonical form
            class_path (String): class path to given service
            pool_size (int): available pool size for service execution
            description (String): short description of what the service does
            initial_state (String): initial state for service
        """
        if not ClaraUtils.is_service_name(service_name):
            raise ValueError("Bad Service name")

        dpe = ClaraUtils.get_dpe_name(service_name)
        container_name = ClaraUtils.get_container_canonical_name(service_name)
        engine_name = ClaraUtils.get_engine_name(service_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe)
        data = ClaraUtils.build_data(CConstants.START_SERVICE,
                                     container_name,
                                     engine_name,
                                     class_path,
                                     pool_size,
                                     description,
                                     initial_state)

        self.base.send(self._create_request(topic, data))

    def remove_service(self, service_name):
        """Sends request to DPE to remove given service

        Args:
            service_name (String): service name in canonical form
        """
        if not ClaraUtils.is_service_name(service_name):
            raise ValueError("Bad Service name")
        dpe_name = ClaraUtils.get_dpe_name(service_name)
        container_name = ClaraUtils.get_container_name(service_name)
        engine_name = ClaraUtils.get_engine_name(service_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        data = ClaraUtils.build_data(CConstants.STOP_SERVICE,
                                     container_name,
                                     engine_name)

        self.base.send(self._create_request(topic, data))

    def execute_service(self, service_name, user_data):
        """Sends request to Service to execute with given data

        Args:
            service_name (String): service name in canonical form
            user_data (EngineData): engine data parameter for service exec
        """
        topic = ClaraUtils.build_topic(CConstants.SERVICE, service_name)
        user_data.metadata.action = xMsgMeta.EXECUTE
        self.base.send(self.base.serialize(topic, user_data, self.datatypes))

    def execute_composition(self, composition, input_data):
        """Sends request to Service to execute with given data

        Args:
            composition (String): service composition for execution
            input_data (EngineData): input data parameter for service execution
        """
        topic = ClaraUtils.build_topic(CConstants.SERVICE,
                                       composition.first_service())
        meta = xMsgMeta()
        meta.MergeFrom(input_data.metadata)
        meta.action = xMsgMeta.EXECUTE
        meta.composition = str(composition)
        input_data.metadata = meta

        message = self.base.serialize(topic, input_data, self.datatypes)
        self.base.send(message)

    def start_reporting_done(self):
        pass

    def start_reporting_data(self):
        pass
