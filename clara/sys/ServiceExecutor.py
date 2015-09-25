#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#

from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.data import xMsgData_pb2

from clara.base.ServiceBase import ServiceBase
from clara.util.CUtility import CUtility

__author__ = 'gurjyan'


class ServiceExecutor(ServiceBase):
    """Service multi-processing class.
    Objects of this class will be stored in the Container's object pool.
    """

    # engine instantiated object
    engine_object = None

    # local copy of the previous composition request,
    # obtained from previously received transient data
    p_composition = xMsgConstants.UNDEFINED

    # the dynamic (updated for every request) repository/map
    # of input-linked service names that are required to be logically AND-ed
    dyn_in_name_list = dict()

    # local map of input-linked services for every
    # composition in multi-composition application.
    # Note: by design compositions are separated by ";"
    in_links = dict()

    # local list of lists output-linked services
    # Note: for output does not matter what composition
    # the output service belongs to. The only thing
    # is to make sure we send only one message to a
    # linked service.
    out_links = []

    def __init__(self, engine_class, container, engine_class_name):
        """Service executor constructor. Does registration request to the local
        Registrar service.

        Params:
            engine_class (String): the name of the python class containing
                service engine class
            container (String): the name of the service container
            engine_class_name (String): the name of the service engine python
                class within the engine_class (container of classes)
        """
        # defines this service canonical name
        service_name = CUtility.form_canonical_name(xMsgUtil.get_local_ip(),
                                                    container,
                                                    engine_class_name)
        ServiceBase.__init__(self, service_name)

        # dynamically loads service engine class
        engine_class = self._for_name(engine_class, engine_class_name)
        self.engine_object = engine_class()

    def run(self, *args):
        """
         Defines which of the methods of the engine interface is requested
         to be executed, by examining transient data "action" field.
         Call execute engine by passing transient data object and composition

        Params:
            in_data_list (String): list of already deserialized protocol-buffer
                data objects de-serialization done at the Broker of this service.
        """

        in_data_list = args
        tr_object = in_data_list[0]

        # check if we have parsed already transient data dynamic
        # routing fields, i.e. "action" and "composition" fields.
        if tr_object.composition != self.p_composition:

            # This is new routing (composition) request,
            # clear local input-link dictionary and output-links list
            self.in_links.clear()
            self.out_links[:] = []

            # store the received composition as previous
            self.p_composition = tr_object.composition

            # parse the new composition to find input and output
            # linked service names, but first check to see if we
            # have multiple parallel compositions (branching)
            if ";" in tr_object.composition:
                l_comps = tr_object.composition.split(";")
                for comp in l_comps:
                    if self.name in comp:
                        self.in_links[comp] = []

                        for x in self.parse_in_linked(self.name, comp):
                            self.in_links[comp].append(x)

                        for y in self.parse_out_linked(self.name, comp):
                            self.out_links.append(y)

            else:
                self.in_links[tr_object.composition] = \
                    self.parse_in_linked(self.name, tr_object.composition)

                self.out_links = self.parse_out_linked(self.name,
                                                       tr_object.composition)

        # execute action request
        if tr_object.action == xMsgData_pb2.Data.EXECUTE:
            self._exec_engine(in_data_list)

        # configure action request
        elif tr_object.action == xMsgData_pb2.Data.CONFIGURE:
            # reset exception parameters
            self.engine_object.reset()
            self.engine_object.configure(tr_object)

    def _exec_engine(self, transient_data):
        """ Checks to see if inputs should be logically "AND"-ed if so, it waits
        and records all received input. If all inputs are present (recorded)
        dynamically loads and executes "execute" method of the engine

        Params:
            transient_data: list of deserialized input transient data object
        """

        # reset exception parameters
        self.engine_object.reset()

        print "executing engine ... "

        if len(transient_data) == 1:

            # single input composition
            new_transient_data = self.engine_object.execute(transient_data[0])
        else:
            # executing the engines execute_group method
            new_transient_data = self.engine_object.execute_group(transient_data)

        new_transient_data.sender = self.name

        self.__service_send(new_transient_data, new_transient_data.id)

    def __service_send(self, transient_data, c_id):

        transient_data.id = c_id

        # send to all output-linked services.
        # Note: service-service communication
        for ss in self.out_links:
            if len(self.out_links) > 1:
                xMsgUtil.sleep(0.01)
            self.send(str(ss), transient_data)

        # check the status of the engine execution and
        # if it is warning or error broadcast exception data
        if transient_data.dataGenerationStatus == xMsgData_pb2.Data.ERROR:
            self.report_data(transient_data, xMsgConstants.ERROR)

        elif transient_data.dataGenerationStatus == xMsgData_pb2.Data.WARNING:
            self.report_data(transient_data, xMsgConstants.WARNING)

        # if data monitors are registered broadcast data
        if transient_data.dataMonitor:
            self.report_data(transient_data, xMsgConstants.INFO)

        # if done monitors are registered broadcast done,
        # informing that service is completed
        if transient_data.doneMonitor:
            self.report_info(xMsgConstants.DONE)

        self.return_object_to_pool()
