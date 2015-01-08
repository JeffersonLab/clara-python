import sys
from core.xMsgConstants import xMsgConstants
from data import xMsgData_pb2
from src.base.OrchestratorBase import OrchestratorBase

__author__ = 'gurjyan'


class Composer(OrchestratorBase):

    """
    """
    engine1 = xMsgConstants.UNDEFINED
    engine2 = xMsgConstants.UNDEFINED
    engine3 = xMsgConstants.UNDEFINED
    engine4 = xMsgConstants.UNDEFINED
    composition = xMsgConstants.UNDEFINED

    def __init__(self, e1, e2, e3, e4, composition):
        OrchestratorBase.__init__(self)
        self.engine1 = e1
        self.engine2 = e2
        self.engine3 = e3
        self.engine4 = e4
        self.composition = composition

    def start(self):

        # create service canonical name from the engine
        l = self.get_service_by_engine(self.engine1)
        if l[0] == xMsgConstants.NO_RESULT:
            print "Engine = " + self.engine1 + " is not registered as a service"
            return
        else:
            service_1 = l[0]

        l = self.get_service_by_engine(self.engine2)
        if l[0] == xMsgConstants.NO_RESULT:
            print "Engine = " + self.engine2 + " is not registered as a service"
            return
        else:
            service_2 = l[0]

        l = self.get_service_by_engine(self.engine3)
        if l[0] == xMsgConstants.NO_RESULT:
            print "Engine = " + self.engine3 + " is not registered as a service"
            return
        else:
            service_3 = l[0]

        l = self.get_service_by_engine(self.engine4)
        if l[0] == xMsgConstants.NO_RESULT:
            print "Engine = " + self.engine4 + " is not registered as a service"
            return
        else:
            service_4 = l[0]

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
        tr.data = 'v'
        tr.dataType = xMsgData_pb2.Data.STRING
        tr.status = xMsgData_pb2.Data.INFO

        print "sending request to " + service_1 + " with the payload: \n" + str(tr)
        self.send(service_1, tr)
        print "sending request to " + service_2 + " with the payload: \n" + str(tr)
        self.send(service_2, tr)
        print "sending request to " + service_3 + " with the payload: \n" + str(tr)
        self.send(service_3, tr)
        print "sending request to " + service_4 + " with the payload: \n" + str(tr)
        self.send(service_4, tr)


def main(e1, e2, e3, e4, cmd):
    orc = Composer(e1, e2, e3, e4, cmd)
    orc.start()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
