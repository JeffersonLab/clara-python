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
from random import randint, uniform


initial_dpe = {
  "DPERuntime": {
    "host": "",
    "snapshot_time": "",
    "cpu_usage": 0,
    "memory_usage": 0,
    "load": 0,
    "containers": []
  }
}


initial_container = {
  "ContainerRuntime": {
    "name": "",
    "snapshot_time": "",
    "n_requests": 0,
    "services": []
  }
}


initial_service = {
  "ServiceRuntime": {
    "name": "",
    "snapshot_time": "",
    "n_requests": 0,
    "n_failures": 0,
    "shm_reads": 0,
    "shm_writes": 0,
    "bytes_recv": 0,
    "bytes_sent": 0,
    "exec_time": 0,
  }
}


D_KEY = "DPERuntime"
C_KEY = "ContainerRuntime"
S_KEY = "ServiceRuntime"
ST_KEY = "snapshot_time"
CC_KEY = "containers"
SS_KEY = "services"
cont_name = "cont_name"
service_name = "cont_name:S1"


class RuntimeDataGenerator(object):

    def __init__(self, name, n_containers, n_services):
        self.n_containers = n_containers
        self.n_services = n_services
        self.data = self._initialize_data_objects(name)

    def _initialize_data_objects(self, name):
        dpe_data = json.loads(json.dumps(initial_dpe))
        containers = [json.loads(json.dumps(initial_container))
                      for _ in range(self.n_containers)]
        services = [json.loads(json.dumps(initial_service))
                    for _ in range(self.n_services)]

        for container in containers:
            container[C_KEY][SS_KEY] = services

        dpe_data[D_KEY][CC_KEY] = containers
        return dpe_data

    def dpe_cpu_usage_random(self):
        return uniform(0, 1)

    def dpe_mem_usage_random(self):
        return uniform(0, 98304)

    def dpe_laod_random(self):
        return uniform(0, 1)

    def cont_request_increase(self):
        return randint(0, 1000)

    def service_request_increase(self):
        return randint(0, 1000)

    def service_failures_increase(self):
        return randint(0, 10)

    def service_bytes_increase(self):
        return randint(0, 1000)

    def service_shm_increase(self):
        return randint(0, 1000)

    def service_exec_time_increase(self):
        return 5000

    def _set_time(self):
        now = str(datetime.now())
        self.data[D_KEY][ST_KEY] = now
        for container in self.data[D_KEY][CC_KEY]:
            container[C_KEY][ST_KEY] = now
            for service in container[C_KEY][SS_KEY]:
                service[S_KEY][ST_KEY] = now

    def get_data(self):
        self._set_time()
        mod_data = self.data
        mod_data[D_KEY]['cpu_usage'] = self.dpe_cpu_usage_random()
        mod_data[D_KEY]['mem_usage'] = self.dpe_mem_usage_random()
        mod_data[D_KEY]['load'] = self.dpe_laod_random()

        for c_index, container in enumerate(mod_data[D_KEY][CC_KEY]):
            container[C_KEY]['name'] = "container_%d" % c_index
            container[C_KEY]['n_requests'] += self.cont_request_increase()
            for s_index, service in enumerate(container[C_KEY][SS_KEY]):
                service[S_KEY]['name'] = "service_%d" % s_index
                service[S_KEY]['n_requests'] += self.service_request_increase()
                service[S_KEY]['n_failures'] += self.service_failures_increase()
                service[S_KEY]['shm_reads'] += self.service_shm_increase()
                service[S_KEY]['shm_writes'] += self.service_shm_increase()
                service[S_KEY]['bytes_recv'] += self.service_bytes_increase()
                service[S_KEY]['bytes_sent'] += self.service_bytes_increase()
                service[S_KEY]['exec_time'] += self.service_exec_time_increase()

        self.data = mod_data
        return json.dumps(mod_data)
