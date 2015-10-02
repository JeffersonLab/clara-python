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

import simplejson as json
from datetime import datetime
from random import randint

initial_dpe = {
  "DPERegistration": {
    "hostname": "",
    "n_cores": randint(24, 96),
    "memory_size": randint(24, 96),
    "language": "java",
    "start_time": str(datetime.now()),
    "containers": []
    }
}

initial_container = {
  "ContainerRegistration": {
    "name": "",
    "language": "java",
    "author": "Dummy Developer",
    "start_time": str(datetime.now()),
    "services": []
  }
}

initial_service = {
  "ServiceRegistration": {
    "class_name": "address.to.the.package.service",
    "engine_name": "da_service",
    "author": "Vardan",
    "version": "1.x",
    "description": "Some LOOOOOOOONG description of what i do",
    "language": "java",
    "start_time": str(datetime.now())
  }
}


D_KEY = "DPERegistration"
C_KEY = "ContainerRegistration"
S_KEY = "ServiceRegistration"
CC_KEY = "containers"
SS_KEY = "services"


class RegistrationDataGenerator(object):

    def __init__(self, name, n_containers, n_services):
        self.name = name
        self._initialize_data_objects(n_containers, n_services)
        self._add_name_tags()

    def _initialize_data_objects(self, n_containers, n_services):
        dpe_data = json.loads(json.dumps(initial_dpe))
        containers = [json.loads(json.dumps(initial_container))
                      for _ in range(n_containers)]
        services = [json.loads(json.dumps(initial_service))
                    for _ in range(n_services)]

        for container in containers:
            container[C_KEY][SS_KEY] = services

        dpe_data[D_KEY][CC_KEY] = containers
        self.data = dpe_data

    def _add_name_tags(self):
        self.data[D_KEY]['hostname'] = self.name
        for c_index, container in enumerate(self.data[D_KEY][CC_KEY]):
            c_name = "%s_java:container_%d" % (self.name, c_index)
            container[C_KEY]['name'] = c_name
            for s_index, service in enumerate(container[C_KEY][SS_KEY]):
                service[S_KEY]['engine_name'] = "%s:service_%d" % (c_name,
                                                                   s_index)

    def get_data(self):
        return json.dumps(self.data)
