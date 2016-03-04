# coding=utf-8
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

from clara.base.ClaraBase import ClaraBase
from clara.name.ServiceName import ServiceName
from clara.sys.Service import Service
from clara.util.ClaraLogger import ClaraLogger


class Container(ClaraBase):
    my_services = {}

    def __init__(self, name, local_address, frontend_address):
        super(Container, self).__init__(name,
                                        local_address.host,
                                        frontend_address.host,
                                        local_address.pub_port,
                                        frontend_address.port)
        self.logger = ClaraLogger(repr(self))
        self.logger.log_info("started: " + self.myname)

    def __repr__(self):
        return str("Container:%s" % self.myname)

    def exit(self):
        self.__remove_services()
        self.logger.log_info("stopped: " + self.myname)

    def add_service(self, engine_name, engine_class, service_pool_size,
                    initial_state):
        service_name = ServiceName(self.myname, engine_name)

        if service_name.name in self.my_services.keys():
            self.logger.log_warning("Service %s already exists. No new"
                                    "service is deployed" % str(service_name))

        else:
            service = Service(service_name.canonical_name(),
                              engine_class, engine_name,
                              service_pool_size, self.default_registrar_address,
                              initial_state, self.default_proxy_address)

            self.my_services[engine_name] = service
            self.logger.log_info("service deployed: " + engine_name)

    def remove_service(self, service_name):
        if service_name in self.my_services.keys():
            service = self.my_services.pop(service_name)
            service.exit()

    def __remove_services(self):
        for service_key in self.my_services.keys():
            self.my_services[service_key].exit()
