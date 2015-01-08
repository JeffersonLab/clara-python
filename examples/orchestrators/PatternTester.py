import sys
from core.xMsgConstants import xMsgConstants
from data import xMsgData_pb2
from src.base.OrchestratorBase import OrchestratorBase


__author__ = 'gurjyan'


class PatternTester(OrchestratorBase):
    """
    This orchestrator is design to test Clara patterns.
    It assumes that services are deployed on the local DPE

    constructor accepts 4 parameters

        Note: all services are assumed to run on a local
              host and have the same container name

        1) the name of the first service engine in the service chain
        2) the name of a container
        2) data size in bytes
        3) actual application composition,
           e.g. s1+s2+s3+s4 or s1,s2,s3+s4
           Note: using engine names only. Actual service names
                 will constructed using the local host and defined
                 container name.
    """
    initiator_engine = xMsgConstants.UNDEFINED
    data_size = 0
    composition = xMsgConstants.UNDEFINED

    def __init__(self, name, data_size, composition):
        OrchestratorBase.__init__(self)
        self.initiator_engine = name
        self.data_size = int(data_size)
        self.composition = composition

    def start(self):

        assert isinstance(self.initiator_engine, str)

        l = self.get_service_by_engine(self.initiator_engine)

        if l[0] == xMsgConstants.NO_RESULT:
            print "Engine = " + self.initiator_engine + " is not registered as a service"
            return
        else:
            service_1 = l[0]

        # recreate composition string by substituting engine
        # names with proper service canonical names
        _cmd = self.engine_to_composition(self.composition)

        # define transient data
        tr = xMsgData_pb2.Data()
        tr.sender = self.get_my_name()
        tr.request_id = 1
        tr.action = xMsgData_pb2.Data.EXECUTE
        tr.composition = _cmd
        # creating a byte buffer using a character as a byte
        tr.data = 'v' * self.data_size
        # tr.data = str(randint(1, 100))
        tr.dataType = xMsgData_pb2.Data.STRING
        tr.dataGenerationStatus = xMsgData_pb2.Data.INFO

        print "sending request to " + service_1 + " with the payload: \n" + str(tr)

        self.send(service_1, tr)


def main(name, d_size, cmd):
    orc = PatternTester(name, d_size, cmd)
    orc.start()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
