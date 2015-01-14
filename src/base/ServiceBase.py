import Queue
from core.xMsgConstants import xMsgConstants
from data import xMsgData_pb2
from src.base.CBase import CBase

__author__ = 'gurjyan'


class ServiceBase(CBase):

    # object pools
    available_object_pool = Queue.Queue()
    used_object_pool = Queue.Queue()

    # initial size of the object pool that will grow
    # based on number of simultaneous requests
    object_pool_size = 1

    """
     The base class for service containers
     Clara service name convention - host:container:name
     Clara service is by design a xMsg subscriber, due
     to the fact that Clara data-flow is a "push" flow.
    """

    def __init__(self, name):
        CBase.__init__(self, name)

    @staticmethod
    def return_object_to_pool():

        """
        Callback is called after objects from the object pool
        inform that the service execution is completed
        """
        try:
            # transfer object from used objects pool to the available pool
            ins = ServiceBase.used_object_pool.get()
            ServiceBase.available_object_pool.put(ins)
        except Queue.Empty:
            pass

    @staticmethod
    def get_object_from_pool():
        """
        Returns the object form the object pool. In case pool is empty
        it will create a new instance of the service class and add to the pool.

        :return: object of the ServiceMP class
        """
        # transfer object from available pool to the used one
        try:
            ins = ServiceBase.available_object_pool.get()
            ServiceBase.used_object_pool.put(ins)
        except Queue.Empty:
            print "available pool is empty"
            return
        return ins


    @staticmethod
    def _for_name(modname, class_name):

        """
        Dynamically loads class "class_name" from module "modname".

        :param modname: the name of the python module
        :param class_name: the name of the python class of the module
        :return dynamically loaded class
        """
        module = __import__(modname)
        classobj = getattr(module, class_name)
        return classobj

    def register(self, dpe_host,
                 container,
                 engine,
                 description=xMsgConstants.UNDEFINED):
        """
        Note that xMsg topic for services are constructed as -
        dpe_host:container:engine

        :param dpe_host: host name of the dpe where service is deployed
        :param container: container name for logical grouping of services
        :param engine: engine name given by the service engine class
        :param description: description of the service
        """
        self.registerSubscriber(self.name,
                                dpe_host,
                                container,
                                engine,
                                description)

    def remove_registration(self, dpe_host,
                            container,
                            engine):
        """
        Removes service xMsg registration

        :param dpe_host: host name of the dpe where service is deployed
        :param container: container name for logical grouping of services
        :param engine: engine name given by the service engine class
        """
        self.removeSubscriberRegistration(self.name,
                                          dpe_host,
                                          container,
                                          engine)

    def report_info(self, info_string):
        """
        Broadcasts a xMsgData transient data
        containing an information string to
        info:sender_canonical_name

        :param info_string: content of the information
        """
        data = xMsgData_pb2.Data()
        data.sender = self.name
        data.dataGenerationStatus = xMsgData_pb2.Data.INFO
        data.dataType = xMsgData_pb2.Data.T_STRING
        data.STRING = str(info_string)
        self.send(xMsgConstants.INFO + ":" +
                  str(self.name),
                  data)

    def report_warning(self, warning_string, severity=1):
        """
        Broadcasts a xMsgData transient data
        containing a warning string to
        warning:sender_canonical_name:severity

        :param warning_string: warning description
        :param severity: severity level
        """
        data = xMsgData_pb2.Data()
        data.sender = self.name
        data.dataGenerationStatus = xMsgData_pb2.Data.WARNING
        data.dataGenerationStatus = severity
        data.dataType = xMsgData_pb2.Data.T_STRING
        data.STRING = str(warning_string)
        self.send(xMsgConstants.WARNING + ":" +
                  str(severity) + ":" +
                  str(self.name),
                  data)

    def report_exception(self, exception_string, severity=1):
        """
        Broadcasts a xMsgData transient data
        containing an error string to
        error:sender_canonical_name:severity

        :param exception_string: error description
        :param severity: severity level
        """
        data = xMsgData_pb2.Data()
        data.sender = self.name
        data.dataGenerationStatus = xMsgData_pb2.Data.ERROR
        data.dataGenerationStatus = severity
        data.dataType = xMsgData_pb2.Data.T_STRING
        data.STRING = str(exception_string)
        self.send(xMsgConstants.ERROR + ":" +
                  str(severity) + ":" +
                  str(self.name),
                  data)

    def report_data(self, data, broadcast_type):
        """
        Broadcasts a xMsgData transient data
        containing data generated by the engine,
        i.e. unaltered user engine output data

        :param data: xMsgData object
        :param broadcast_type: defines the topic to which
                            data will be broadcast. Only
                            xMsgConstants.INFO/WARNING/ERROR
                            are supported.
        """
        severity = str(1)

        if broadcast_type is xMsgConstants.INFO:
            self.send(xMsgConstants.INFO + ":" +
                      str(self.name),
                      data)
        elif broadcast_type is xMsgConstants.WARNING:
            self.send(xMsgConstants.WARNING + ":" +
                      str(severity) + ":" +
                      str(self.name),
                      data)
        elif broadcast_type is xMsgConstants.ERROR:
            self.send(xMsgConstants.ERROR + ":" +
                      str(severity) + ":" +
                      str(self.name),
                      data)