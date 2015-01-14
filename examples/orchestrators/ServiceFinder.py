from core.xMsgUtil import xMsgUtil
from src.base.OrchestratorBase import OrchestratorBase

__author__ = 'gurjyan'


class ServiceFinder(OrchestratorBase):
    def __init__(self):
        OrchestratorBase.__init__(self)

    def start(self):

        while True:
            xMsgUtil.sleep(1)
            print "acceptable commands: getServiceByName, getServiceByEngineName, " \
                  "getServicesByContainer, getServicesByHost"
            cmd = raw_input("enter a command:")
            if cmd == "getServiceByName":
                service_name = raw_input("what is the canonical name of the service?")
                lr_data = self.find_service(service_name)
                print lr_data[0]

            elif cmd == "getServiceByEngineName":
                engine_name = raw_input("what is the service engine name?")
                lr_data = self.get_service_by_engine(engine_name)
                for d in lr_data:
                    print d

            elif cmd == "getServicesByContainer":
                container_name = raw_input("what is the canonical name of the container?")
                lr_data = self.get_service_by_container(container_name)
                for d in lr_data:
                    print d

            elif cmd == "getServicesByHost":
                host_name = raw_input("what is the IP of the host?")
                lr_data = self.get_service_by_host(host_name)
                for d in lr_data:
                    print d

def main():
    o = ServiceFinder()
    o.start()


if __name__ == '__main__':
    main()
