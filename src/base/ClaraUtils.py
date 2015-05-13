'''
Created on 11-05-2015

@author: royarzun
'''
import re
from src.util.CConstants import CConstants

CANONICAL_NAME_PATTERN = "^([^:_ ]+_(java|python|cpp))(:(\\w+)(:(\\w+))?)?$"
CANONICAL_NAME_VALIDATOR = re.compile(CANONICAL_NAME_PATTERN)


class ClaraUtils():

    def __init__(self, params):
        pass

    @staticmethod
    def isDpeName(name):
        dpe_name = CANONICAL_NAME_VALIDATOR.match(name)
        if dpe_name and len(name.split(CConstants.TOPIC_SEP)) == 1:
            return True
        else:
            return False

    @staticmethod
    def isContainerName(name):
        container_name = CANONICAL_NAME_VALIDATOR.match(name)
        if container_name and len(name.split(CConstants.TOPIC_SEP)) == 2:
            return True
        else:
            return False

    @staticmethod
    def isServiceName(name):
        service_name = CANONICAL_NAME_VALIDATOR.match(name)
        if service_name and len(name.split(CConstants.TOPIC_SEP)) == 3:
            return True
        else:
            return False

    @staticmethod
    def getHostname(canonical_name):
        dpe_name = canonical_name.split(CConstants.TOPIC_SEP)[0]
        return dpe_name.split(CConstants.LANG_SEP)[0]

    @staticmethod
    def getDpeName(canonical_name):
        return canonical_name.split(CConstants.TOPIC_SEP)[0]

    @staticmethod
    def getContainerCanonicalName(canonical_name):
        match = CANONICAL_NAME_VALIDATOR.match(canonical_name)
        return match.group(1) + CConstants.TOPIC_SEP + match.group(4)

    @staticmethod
    def getContainerName(canonical_name):
        return CANONICAL_NAME_VALIDATOR.match(canonical_name).group(4)

    @staticmethod
    def getEngineName(canonical_name):
        return CANONICAL_NAME_VALIDATOR.match(canonical_name).group(5)

    @staticmethod
    def formDpeName(host, lang):
        return host + CConstants.LANG_SEP + lang

    @staticmethod
    def formContainerName(dpe_name, container_name):
        return dpe_name + CConstants.TOPIC_SEP + container_name

    @staticmethod
    def formServiceName(container_name, service_engine):
        return container_name + CConstants.TOPIC_SEP + service_engine    
