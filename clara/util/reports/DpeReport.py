# coding=utf-8

import json
from multiprocessing import cpu_count

from psutil import virtual_memory, cpu_percent

from clara.util.CConstants import CConstants
from clara.util.reports.BaseReport import BaseReport


class DpeReport(BaseReport):

    _containers = dict()
    run_exclude = ["clara_home"]
    reg_exclude = ["memory_usage", "cpu_usage", "load", "description", "name",
                   "snapshot_time", "service_count", "author",
                   "failure_count", "shm_reads", "shm_writes", "bytes_received",
                   "bytes_sent", "execution_time"]

    def __init__(self, base, author):
        super(DpeReport, self).__init__(base.myname, author)
        self.hostname = self.name
        self.clara_home = base.clara_home
        self.n_cores = cpu_count()
        self.memory_size = virtual_memory().total

    def add_container(self, container_report):
        if container_report.name not in self._containers:
            self._containers[container_report.name] = container_report

    def get_alive_data(self):
        return self.name + CConstants.DATA_SEP + \
               str(self.n_cores) + CConstants.DATA_SEP + self.clara_home

    def get_containers(self):
        return self._containers.values()

    def remove_container(self, container_report):
        self._containers.pop(container_report.name)

    def remove_containers(self):
        self._containers.clear()

    def _refresh(self):
        self.cpu_usage = cpu_percent()
        self.load = 0
        self.memory_usage = virtual_memory().used
        self.containers = [container.to_str() for container in
                           self.get_containers()]

    def to_json(self):
        self._refresh()
        dpe_dict = dict()
        dpe_dict["DPERuntime"] = self.as_dict(self.run_exclude)
        dpe_dict["DPERegistration"] = self.as_dict(self.reg_exclude)
        return json.dumps(dpe_dict, sort_keys=True, indent=4)
