# coding=utf-8

import json
from multiprocessing import cpu_count

from psutil import virtual_memory, cpu_percent

from clara.util.CConstants import CConstants
from clara.util.reports.BaseReport import BaseReport


class DpeReport(BaseReport):

    _containers = dict()

    def __init__(self, base, author):
        super(DpeReport, self).__init__(base.myname, author)
        self.host = self.name
        self.clara_home = base.clara_home
        self.core_count = cpu_count()
        self.memory_size = virtual_memory().total
        self.alive_data = self.name + CConstants.DATA_SEP +\
            str(self.core_count) + CConstants.DATA_SEP + self.clara_home

    def add_container(self, container_report):
        if container_report.name not in self._containers:
            self._containers[container_report.name] = container_report

    def get_alive_data(self):
        return self.alive_data

    def get_containers(self):
        return self._containers.values()

    def remove_container(self, container_report):
        self._containers.pop(container_report.name)

    def remove_containers(self):
        self._containers.clear()

    def _refresh(self):
        self.cpu_usage = cpu_percent()
        self.memory_usage = virtual_memory().used
        self.containers = [container.to_str() for container in
                           self._containers.values()]

    def to_json(self):
        self._refresh()
        return json.dumps(self.as_dict(), sort_keys=True, indent=4)
