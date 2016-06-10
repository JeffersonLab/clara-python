# coding=utf-8

from abc import ABCMeta, abstractmethod
from xmsg.core.xMsgConstants import xMsgConstants

from clara.base.ClaraAddress import ClaraAddress
from clara.base.ClaraLang import ClaraLang
from clara.util.CConstants import CConstants


class ClaraName(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def canonical_name(self):
        pass

    @abstractmethod
    def name(self):
        pass


class DpeName(ClaraName):

    def __init__(self, host, port, language=ClaraLang.PYTHON):
        self.__dpe_language = language
        self.__dpe_address = ClaraAddress(host, port)

        if port != int(xMsgConstants.DEFAULT_PORT):
            port = "%" + str(port)
            self.__name = "%s%s%s%s" % (host, port,
                                        CConstants.LANG_SEP, language)
        else:
            self.__name = "%s%s%s" % (host, CConstants.LANG_SEP, language)

    def __str__(self):
        return self.__name

    def name(self):
        return self.__name

    def canonical_name(self):
        return self.__name

    def language(self):
        return self.__dpe_language

    def address(self):
        return self.__dpe_address


class ContainerName(ClaraName):

    def __init__(self, dpe, name):
        if not isinstance(dpe, DpeName):
            raise TypeError("dpe argument must be of type DpeName")
        else:
            self.__canonical_name = str(dpe) + CConstants.TOPIC_SEP + str(name)
            self.__name = name
            self.__dpe = dpe

    def __str__(self):
        return self.canonical_name()

    def canonical_name(self):
        return self.__canonical_name

    def name(self):
        return self.__name

    def get_dpe_name(self):
        return self.__dpe


class ServiceName(ClaraName):

    def __init__(self, container, engine):
        if not isinstance(container, ContainerName):
            raise TypeError("container argument must be of type ContainerName")

        else:
            self.__name = str(container) + CConstants.TOPIC_SEP + str(engine)
            self.__engine = engine
            self.__container = container

    def __str__(self):
        return self.__name

    def canonical_name(self):
        return self.__name

    def name(self):
        return self.__engine

    def get_container_name(self):
        return self.__container
