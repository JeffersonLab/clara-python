# coding=utf-8

from abc import ABCMeta, abstractmethod
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.data.xMsgMeta_pb2 import xMsgMeta

from clara.base.error.ClaraException import ClaraException
from clara.base.ClaraUtils import ClaraUtils
from clara.util.CConstants import CConstants


class BaseRequest(object):
    __metaclass__ = ABCMeta
    __meta = xMsgMeta()
    __base = xMsgConstants.UNDEFINED
    __topic = xMsgConstants.UNDEFINED
    __frontend = xMsgConstants.UNDEFINED

    def __init__(self, base, frontend, topic):
        self.__frontend = frontend
        self.__topic = topic
        self.__base = base

    @abstractmethod
    def msg(self):
        pass

    @abstractmethod
    def parse_data(self, msg):
        pass

    def run(self):
        try:
            self.__base.send(self.__frontend, self.msg())
        except Exception as e:
            raise ClaraException("cannot send message: %s" % e)

    def sync_run(self, timeout_in_ms):
        try:
            response = self.__base.sync_send(self.__frontend, timeout_in_ms)
            return self.parse_data(response)
        except Exception as e:
            raise ClaraException("cannot send message: %s" % e)


class DataRequest(BaseRequest):
    __metaclass__ = ABCMeta

    def __init__(self, base, frontend, topic):
        super(DataRequest, self).__init__(base, frontend, topic)

    @abstractmethod
    def get_data(self):
        pass

    def msg(self):
        return __create_message(self.topic, self.get_data())

    def parse_data(self, msg):
        return True


class DeployRequest(DataRequest):

    def __init__(self, base, frontend, topic):
        super(DeployRequest, self).__init__(base, frontend, topic)

    def with_pool_size(self, pool_size):
        self.__poolsize = pool_size
        return self

    def with_description(self, description):
        self.description = description
        return self


class DeployContainerRequest(DeployRequest):
    __container = ""

    def __init__(self, base, frontend, topic):
        super(DeployContainerRequest, self).__init__(base, frontend, topic)
        self.__container_name = topic

    def get_data(self):
        return ClaraUtils.build_data(CConstants.START_CONTAINER,
                                     self.__container.name(),
                                     self.__poolsize,
                                     self.description)


class DeployServiceRequest(DeployRequest):
    __service = ""
    __class_path = ""
    __initial_state = CConstants.UNDEFINED

    def __init__(self, base, frontend, service, class_path):
        super(DeployServiceRequest, self).__init__(base, frontend, service)
        self.__service = service
        self.__class_path = class_path

    def with_initial_state(self, initial_state):
        self.__initial_state = initial_state
        return self

    def get_data(self):
        return ClaraUtils.build_data(CConstants.START_SERVICE,
                                     self.__service_name,
                                     self.__service.name(),
                                     self.__class_path,
                                     self.__poolsize,
                                     self.description,
                                     self.__initial_state)


def __get_dpe_topic(component_name):
    return str(ClaraUtils.get_dpe_name(component_name))


def __create_message(topic, data):
    try:
        return xMsgMessage(topic, str(data))
    except Exception as e:
        raise ClaraException("Cannot create message: " + e)
