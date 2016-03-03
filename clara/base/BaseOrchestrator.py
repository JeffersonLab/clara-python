#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
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
from xmsg.core.xMsgConstants import xMsgConstants

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraUtils import ClaraUtils
from clara.util.CConstants import CConstants


class BaseOrchestrator(object):
    base = CConstants.UNDEFINED
    name = CConstants.UNDEFINED

    def __init__(self, fe_host="localhost", pool_size=2):
        self.fe_host = fe_host
        self.pool_size = pool_size
        self.name = BaseOrchestrator.generate_name()
        self.base = self.__get_clara_base()

    @staticmethod
    def generate_name():
        return "orchestrator_%d" % (random.randint(0, 1000))

    def __get_clara_base(self):
        localhost = ClaraUtils.localhost()
        return ClaraBase(self.name, localhost, localhost,
                         int(xMsgConstants.DEFAULT_PORT),
                         int(xMsgConstants.DEFAULT_PORT))

    def __create_request(self, topic, data):
        msg = xMsgMessage(topic)
        msg.set_data(data, "text/string")
        return msg

    def exit_dpe(self, dpe_name):
        if not ClaraUtils.is_dpe_name(dpe_name):
            raise MalformedCanonicalName("Malformed DPE name: %s" % dpe_name)
        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        self.base.send(xMsgMessage(topic, CConstants.DPE_EXIT))

    def deploy_container(self, container_name, pool_size=2, description=None):
        if not ClaraUtils.is_container_name(container_name):
            raise ValueError("Bad Container name")

        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe)
        data = ClaraUtils.build_data(CConstants.START_CONTAINER,
                                     name, pool_size, description)

        self.base.send(self.__create_request(topic, data))

    def deploy_container_sync(self):
        pass

    def exit_container(self, container_name):
        if not ClaraUtils.is_container_name(container_name):
            raise ValueError("Bad Container name")

        dpe = ClaraUtils.get_dpe_name(container_name)
        name = ClaraUtils.get_container_name(container_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe)
        data = ClaraUtils.build_data(CConstants.STOP_CONTAINER, name)

        self.base.send(self.__create_request(topic, data))

    def exit_container_sync(self):
        pass

    def deploy_service(self, service_name, class_path, pool_size=1,
                       description=None, initial_state=CConstants.UNDEFINED):
        if not ClaraUtils.is_service_name(service_name):
            raise ValueError("Bad Service name")

        dpe = ClaraUtils.get_dpe_name(service_name)
        container_name = ClaraUtils.get_container_name(service_name)
        engine_name = ClaraUtils.get_engine_name(service_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe)
        data = ClaraUtils.build_data(CConstants.START_SERVICE,
                                     container_name,
                                     engine_name,
                                     class_path,
                                     pool_size,
                                     description,
                                     initial_state)

        self.base.send(self.__create_request(topic, data))

    def deploy_service_sync(self):
        pass

    def remove_service(self, service_name):
        if not ClaraUtils.is_service_name(service_name):
            raise ValueError("Bad Service name")
        dpe_name = ClaraUtils.get_dpe_name(service_name)
        container_name = ClaraUtils.get_container_name(service_name)
        engine_name = ClaraUtils.get_engine_name(service_name)

        topic = ClaraUtils.build_topic(CConstants.DPE, dpe_name)
        data = ClaraUtils.build_data(CConstants.STOP_SERVICE,
                                     container_name,
                                     engine_name)
        self.base.send(self.__create_request(topic, data))

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
