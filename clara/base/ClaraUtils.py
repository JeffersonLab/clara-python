#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
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

import re
from xmsg.core.xMsgUtil import xMsgUtil

from clara.base.CConstants import CConstants


CNAME_PATTERN = "^([^:_ ]+_(java|python|cpp))(:(\\w+)(:(\\w+))?)?$"
CNAME_VALIDATOR = re.compile(CNAME_PATTERN)


class ClaraUtils:

    @staticmethod
    def is_dpe_name(name):
        return bool(CNAME_VALIDATOR.match(name) and
                    len(name.split(CConstants.TOPIC_SEP)) is 1)

    @staticmethod
    def is_container_name(name):
        return bool(CNAME_VALIDATOR.match(name) and
                    len(name.split(CConstants.TOPIC_SEP)) is 2)

    @staticmethod
    def is_service_name(name):
        return bool(CNAME_VALIDATOR.match(name) and
                    len(name.split(CConstants.TOPIC_SEP)) is 3)

    @staticmethod
    def get_hostname(canonical_name):
        dpe_name = canonical_name.split(CConstants.TOPIC_SEP)[0]
        return dpe_name.split(CConstants.LANG_SEP)[0]

    @staticmethod
    def get_dpe_name(canonical_name):
        return canonical_name.split(CConstants.TOPIC_SEP)[0]

    @staticmethod
    def get_container_canonical_name(canonical_name):
        match = CNAME_VALIDATOR.match(canonical_name)
        return match.group(1) + CConstants.TOPIC_SEP + match.group(4)

    @staticmethod
    def get_container_name(canonical_name):
        return CNAME_VALIDATOR.match(canonical_name).group(4)

    @staticmethod
    def get_engine_name(canonical_name):
        return CNAME_VALIDATOR.match(canonical_name).group(5)

    @staticmethod
    def form_dpe_name(host, lang):
        return host + CConstants.LANG_SEP + str(lang)

    @staticmethod
    def form_container_name(dpe_name, container_name):
        return dpe_name + CConstants.TOPIC_SEP + container_name

    @staticmethod
    def form_service_name(container_name, service_engine):
        return container_name + CConstants.TOPIC_SEP + service_engine

    @staticmethod
    def is_host_local(hostname):
        if str(hostname) in xMsgUtil.get_local_ips():
            return True

        else:
            return False

    @staticmethod
    def build_data(*args):
        topic = [str(arg) for _, arg in enumerate(args)]
        return "?".join(topic)

    @staticmethod
    def build_topic(*args):
        topic = [str(arg) for _, arg in enumerate(args)]
        return ":".join(topic)
