import os
import sys
from core.xMsgConstants import xMsgConstants
from data import xMsgData_pb2
from data.xMsgData_pb2 import Data
from src.base.OrchestratorBase import OrchestratorBase


__author__ = 'gurjyan'


class Configurator(OrchestratorBase):

    engine1 = xMsgConstants.UNDEFINED
    engine2 = xMsgConstants.UNDEFINED
    engine3 = xMsgConstants.UNDEFINED
    engine4 = xMsgConstants.UNDEFINED
    engine5 = xMsgConstants.UNDEFINED
    container = xMsgConstants.UNDEFINED

    def __init__(self, e1, e2, e3, e4, e5):
        OrchestratorBase.__init__(self)
        self.engine1 = e1
        self.engine2 = e2
        self.engine3 = e3
        self.engine4 = e4
        self.engine5 = e5
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
        l = self.get_service_by_engine(self.engine5)
        if l[0] == xMsgConstants.NO_RESULT:
            print "Engine = " + self.engine5 + " is not registered as a service"
            return
        else:
            service_5 = l[0]

        tr = xMsgData_pb2.Data()
        tr.sender = self.name
        tr.id = 1
        tr.action = xMsgData_pb2.Data.CONFIGURE
        tr.dataType = xMsgData_pb2.Data.T_STRING
        tr.dataGenerationStatus = xMsgData_pb2.Data.INFO
        tr.STRING = os.environ["PCLARA_HOME"] + "/examples/engines/Data/d1.txt"
        print "sending configure request to " + service_1.name + " with the payload: \n" + str(tr)
        self.send(service_1.name, tr)
        tr.STRING = os.environ["PCLARA_HOME"] + "/examples/engines/Data/d2.txt"
        print "sending configure request to " + service_2.name + " with the payload: \n" + str(tr)
        self.send(service_2.name, tr)
        tr.STRING = os.environ["PCLARA_HOME"] + "/examples/engines/Data/d3.txt"
        print "sending configure request to " + service_3.name + " with the payload: \n" + str(tr)
        self.send(service_3.name, tr)
        tr.STRING = os.environ["PCLARA_HOME"] + "/examples/engines/Data/d4.txt"
        print "sending configure request to " + service_4.name + " with the payload: \n" + str(tr)
        self.send(service_4.name, tr)
        print "sending configure request to " + service_5.name + " with the payload: \n" + str(tr)
        self.send(service_5.name, tr)


def main(n1, n2, n3, n4, n5):
    Configurator(n1, n2, n3, n4, n5)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
