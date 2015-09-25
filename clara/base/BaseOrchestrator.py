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

import random
from xmsg.core.xMsgExceptions import MalformedCanonicalName
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.core.xMsgTopic import xMsgTopic

from clara.base.ClaraUtils import ClaraUtils
from clara.base.CConstants import CConstants
from clara.base.CBase import CBase


class BaseOrchestrator(object):

    def __init__(self, fe_host="localhost"):
        self.base = self.__get_clara_base(fe_host)

    def _build_data(self, *data_array):
        topic = ""
        for index, data in enumerate(data_array[0:]):
            if index != 1:
                topic = topic + str(CConstants.TOPIC_SEP) + str(data)

            else:
                topic = str(data)

        return topic
    
    def _build_message(self):
        pass

    def _generate_name(self):
        return "orchestrator%s:localhost" % str(random.randint(0, 1000))

    def __get_clara_base(self, fe_host):
        return CBase(self._generate_name(), fe_host)

    def exit_dpe(self, dpe_name):
        if not ClaraUtils.is_dpe_name(dpe_name):
            raise MalformedCanonicalName("Malformed DPE name: %s"
                                         % str(dpe_name))
        host = ClaraUtils.get_hostname(dpe_name)
        topic = self.__build_topic(str(CConstants.DPE), dpe_name)
        data = str(CConstants.DPE_EXIT)

        msg = xMsgMessage.create_with_serialized_data(topic, data)
        self.base.send(msg)

    def deploy_container(self, container_name):
        if not ClaraUtils.is_container_name(container_name):
            raise ValueError("Bad Container name")

        host = ClaraUtils.get_hostname(container_name)
        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)
        
        topic = xMsgTopic.wrap(str(CConstants.DPE)+dpe)
        data = self._build_data(str(CConstants.START_CONTAINER)+name)
        
        msg = xMsgMessage(topic, data)
        
        try:
            self.base.generic_send(msg)

        except Exception as e:
            raise Exception("Orchestrator could not send the request: %s" % e)

    def deploy_container_sync(self):
        pass

    def remove_container(self):
        pass

    def remove_container_sync(self):
        pass

    def deploy_service(self):
        pass

    def deploy_service_sync(self):
        pass

    def remove_service(self):
        pass

    def remove_service_sync(self):
        pass

    def configure_service(self):
        pass

    def configure_service_sync(self):
        pass

    def execute_service(self):
        pass

    def execute_service_sync(self):
        pass

    def execute_composition(self):
        pass

    def execute_composition_sync(self):
        pass

    def start_reporting_done(self):
        pass

    def start_reporting_data(self):
        pass
