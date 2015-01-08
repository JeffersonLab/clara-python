from src.base.OrchestratorBase import OrchestratorBase
from src.util.CUtility import CUtility

__author__ = 'gurjyan'


class ServiceFinder(OrchestratorBase):
    def __init__(self):
        OrchestratorBase.__init__(self)

    def start(self):

        while True:
            CUtility.sleep(1)
            print "acceptable commands: getServiceByName, getServiceByEngineName, " \
                  "getServicesByContainer, getServicesByHost"
            cmd = raw_input("enter a command:")
            if cmd == "getServiceByName":
                service_name = raw_input("what is the canonical name of the service?")
                print self.find_service(service_name)

            elif cmd == "getServiceByEngineName":
                engine_name = raw_input("what is the service engine name?")
                print self.get_service_by_engine(engine_name)

            elif cmd == "getServicesByContainer":
                container_name = raw_input("what is the canonical name of the container?")
                print self.get_service_by_container(container_name)

            elif cmd == "getServicesByHost":
                host_name = raw_input("what is the IP of the host?")
                print self.get_service_by_host(host_name)


def main():
    o = ServiceFinder()
    o.start()


if __name__ == '__main__':
    main()
