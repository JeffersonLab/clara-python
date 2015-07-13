'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''
import Queue
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.data import xMsgData_pb2

from clara.base.CBase import CBase

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

    def register(self, dpe_host, container, engine,
                 description=str(xMsgConstants.UNDEFINED)):
        """
        Note that xMsg topic for services are constructed as -
        dpe_host:container:engine

        :param dpe_host: host name of the dpe where service is deployed
        :param container: container name for logical grouping of services
        :param engine: engine name given by the service engine class
        :param description: description of the service
        """
        topic = xMsgTopic.build(dpe_host, container, engine)
        self.register_subscriber(topic, description)

    def remove_registration(self, dpe_host, container, engine):
        """
        Removes service xMsg registration

        :param dpe_host: host name of the dpe where service is deployed
        :param container: container name for logical grouping of services
        :param engine: engine name given by the service engine class
        """
        topic = xMsgTopic.build(dpe_host, container, engine)
        self.remove_subscriber_registration(topic)

    def report_info(self, info_string):
        """
        Broadcasts a xMsgData transient data
        containing an information string to
        info:sender_canonical_name

        :param info_string: content of the information
        """
        data = xMsgData_pb2.xMsgData()
        data.sender = self.name
        data.dataGenerationStatus = xMsgData_pb2.xMsgData.INFO
        data.dataType = xMsgData_pb2.xMsgData.T_STRING
        data.STRING = str(info_string)
        self.send(xMsgConstants.INFO + ":" + str(self.name), data)

    def report_warning(self, warning_string, severity=1):
        """
        Broadcasts a xMsgData transient data
        containing a warning string to
        warning:sender_canonical_name:severity

        :param warning_string: warning description
        :param severity: severity level
        """
        data = xMsgData_pb2.xMsgData()
        data.sender = self.name
        data.dataGenerationStatus = xMsgData_pb2.xMsgData.WARNING
        data.dataGenerationStatus = severity
        data.dataType = xMsgData_pb2.xMsgData.T_STRING
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
        data = xMsgData_pb2.xMsgData()
        data.sender = self.name
        data.dataGenerationStatus = xMsgData_pb2.xMsgData.ERROR
        data.dataGenerationStatus = severity
        data.dataType = xMsgData_pb2.xMsgData.T_STRING
        data.STRING = str(exception_string)
        self.send(xMsgConstants.ERROR + ":" +
                  str(severity) + ":" +
                  str(self.name),
                  data)
        self._report_message(xMsgConstants.ERROR)

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

        if broadcast_type is str(xMsgConstants.INFO):
            self.send(str(xMsgConstants.INFO) + ":" +
                      str(self.name),
                      data)
        elif broadcast_type is str(xMsgConstants.WARNING):
            self.send(str(xMsgConstants.WARNING) + ":" +
                      str(severity) + ":" +
                      str(self.name),
                      data)
        elif broadcast_type is str(xMsgConstants.ERROR):
            self.send(str(xMsgConstants.ERROR) + ":" +
                      str(severity) + ":" +
                      str(self.name),
                      data)
