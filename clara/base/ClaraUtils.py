'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''
import re

from clara.base.CConstants import CConstants

CNAME_PATTERN = "^([^:_ ]+_(java|python|cpp))(:(\\w+)(:(\\w+))?)?$"
CNAME_VALIDATOR = re.compile(CNAME_PATTERN)


class ClaraUtils():

    @staticmethod
    def isDpeName(name):
        return bool(CNAME_VALIDATOR.match(name) and
                    len(name.split(CConstants.TOPIC_SEP)) is 1)

    @staticmethod
    def isContainerName(name):
        return bool(CNAME_VALIDATOR.match(name) and
                    len(name.split(CConstants.TOPIC_SEP)) is 2)

    @staticmethod
    def isServiceName(name):
        return bool(CNAME_VALIDATOR.match(name) and
                    len(name.split(CConstants.TOPIC_SEP)) is 3)

    @staticmethod
    def getHostname(canonical_name):
        dpe_name = canonical_name.split(CConstants.TOPIC_SEP)[0]
        return dpe_name.split(CConstants.LANG_SEP)[0]

    @staticmethod
    def getDpeName(canonical_name):
        return canonical_name.split(CConstants.TOPIC_SEP)[0]

    @staticmethod
    def getContainerCanonicalName(canonical_name):
        match = CNAME_VALIDATOR.match(canonical_name)
        return match.group(1) + CConstants.TOPIC_SEP + match.group(4)

    @staticmethod
    def getContainerName(canonical_name):
        return CNAME_VALIDATOR.match(canonical_name).group(4)

    @staticmethod
    def getEngineName(canonical_name):
        return CNAME_VALIDATOR.match(canonical_name).group(5)

    @staticmethod
    def formDpeName(host, lang):
        return host + CConstants.LANG_SEP + str(lang)

    @staticmethod
    def formContainerName(dpe_name, container_name):
        return dpe_name + CConstants.TOPIC_SEP + container_name

    @staticmethod
    def formServiceName(container_name, service_engine):
        return container_name + CConstants.TOPIC_SEP + service_engine
