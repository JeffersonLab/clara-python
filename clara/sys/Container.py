# coding=utf-8

from getpass import getuser

from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraNames import ServiceName
from clara.sys.Service import Service
from clara.util.ClaraLogger import ClaraLogger
from clara.util.reports.ContainerReport import ContainerReport


class Container(ClaraBase):
    my_services = dict()

    def __init__(self, container_name, local_address, frontend_address):
        super(Container, self).__init__(container_name.canonical_name(),
                                        local_address.host,
                                        local_address.pub_port,
                                        frontend_address.host,
                                        frontend_address.pub_port)
        self._container_name = container_name
        self._logger = ClaraLogger(repr(self))
        self._logger.log_info("container deployed")
        self._report = ContainerReport(self, getuser())

    def __repr__(self):
        return str("Container:%s" % self.myname)

    def exit(self):
        self._remove_services()
        self._logger.log_info("container stopped")

    def add_service(self, engine_name, engine_class, service_pool_size,
                    initial_state):
        service_name = ServiceName(self._container_name, engine_name)

        if service_name.canonical_name() in self.my_services:
            self._logger.log_warning("Service %s already exists. No new "
                                     "service is deployed" % str(service_name))
        else:
            try:
                service = Service(service_name,
                                  engine_class,
                                  engine_name,
                                  service_pool_size,
                                  initial_state,
                                  self._proxy_address,
                                  self._fe_address)
                self.my_services[service_name.canonical_name()] = service
                self._report.add_service(service.get_report())

            except Exception as e:
                self._logger.log_exception("%s: %s" % (str(service_name), e))
                raise e

    def get_report(self):
        return self._report

    def remove_service(self, service_name):
        if service_name in self.my_services:
            service = self.my_services.pop(service_name)
            self._report.remove_service(service.get_report())
            service.exit()

    def _remove_services(self):
        for service in self.my_services.itervalues():
            service.exit()
