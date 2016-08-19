# coding=utf-8

from clara.util.reports.BaseReport import BaseReport


class ContainerReport(BaseReport):
    services = dict()

    def __init__(self, base, author):
        super(ContainerReport, self).__init__(base.myname, author, "")

    def get_service_count(self):
        return len(self.services)

    def get_services(self):
        return self.services.values()

    def add_service(self, service_report):
        if not self.services.has_key(service_report.engine_name):
            self.services[service_report.engine_name] = service_report

    def remove_service(self, service_report):
        self.services.pop(service_report.engine_name)

    def remove_services(self):
        self.services.clear()
