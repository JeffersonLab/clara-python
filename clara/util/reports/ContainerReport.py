# coding=utf-8

import json

from clara.util.reports.BaseReport import BaseReport


class ContainerReport(BaseReport):

    _services = dict()

    def __init__(self, base, author):
        super(ContainerReport, self).__init__(base.myname, author, "")
        self.service_count = 0

    def get_services(self):
        return self._services.values()

    def add_service(self, service_report):
        if service_report.name not in self._services:
            self._services[service_report.engine_name] = service_report

    def remove_service(self, service_report):
        self._services.pop(service_report.engine_name)

    def remove_services(self):
        self._services.clear()

    def _refresh(self):
        self.services = [service.to_str() for service in
                         self._services.values()]
        self.service_count = len(self._services)

    def to_json(self):
        self._refresh()
        return json.dumps(self.as_dict(), indent=4, sort_keys=True)

    def to_str(self):
        self._refresh()
        return self.as_dict()
