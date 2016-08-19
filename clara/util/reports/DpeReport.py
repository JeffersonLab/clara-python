# coding=utf-8

from multiprocessing import cpu_count

from psutil import virtual_memory, cpu_percent

from clara.util.CConstants import CConstants
from clara.util.reports.BaseReport import BaseReport


class DpeReport(BaseReport):

    _containers = dict()

    def __init__(self,base, author):
        super(DpeReport, self).__init__(base.myname, author, "")
        self._host = self.name
        self._clara_home = base.clara_home
        self._core_count = cpu_count()
        self._memory_size = virtual_memory().total
        self._alive_data = self.name + CConstants.DATA_SEP +\
            self._core_count + CConstants.DATA_SEP + self._clara_home

    def add_container(self, container_report):
        if not self._containers.has_key(container_report.name):
            self._containers[container_report.name] = container_report

    def get_alive_data(self):
        return self._alive_data

    def get_host(self):
        return self._host

    def get_clara_home(self):
        return self._clara_home

    def get_containers(self):
        return self._containers.values()

    def get_core_count(self):
        return self._core_count

    def get_cpu_usage(self):
        return cpu_percent()

    def get_load(self):
        return ""

    def get_memory_size(self):
        return self._memory_size

    def get_memory_usage(self):
        return virtual_memory().used

    def remove_container(self, container_report):
        self._containers.pop(container_report.name)

    def remove_containers(self):
        self._containers.clear()
