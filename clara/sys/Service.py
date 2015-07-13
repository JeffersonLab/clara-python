from copy import deepcopy
import threading
import sys
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from data import xMsgData_pb2
from src.base.ServiceBase import ServiceBase
from src.sys.ServiceExecutor import ServiceExecutor

from src.util.CUtility import CUtility


__author__ = 'gurjyan'


class Service(ServiceBase):
    """
    Service container/broker class. This creates ServiceMP object pool.
    Handles subscriptions and callbacks.
    Calls service (service executor) object's run method in a separate thread.
    """

    def __init__(self, engine_class, container, engine_class_name, p_size):
        """
                Service constructor.
                Does registration request to the local Registrar service.

                :param engine_class: the name of the python class containing
                                               service engine class
                :param container: the name of service container, for logical grouping of services.
                :param engine_class_name: the name of the service engine python class
                                        within the engine_container_class
                :param p_size: Service object pool size, i.e. number of parallel services
                """

        # local copy of the previous composition request,
        # obtained from previously received transient data
        self.p_composition = xMsgConstants.UNDEFINED

        # the dynamic (updated for every request) repository/map
        # of input-linked service names that are required to be logically AND-ed
        self.dyn_in_name_list = dict()

        # the dynamic ( updated for every request) repository/map
        # of input-linked service data that are required to be logically AND-ed
        self.dyn_in_data_list = dict()

        # local map of input-linked services for every
        # composition in multi-composition application.
        # Note: by design compositions are separated by ";"
        self.in_links = dict()

        # local boolean indicating that service has multiple
        # inputs and they are required to be logically ANDed
        self.log_and_request = False

        # user provided engine class container class name
        self.engine_class = engine_class

        # the name of the CLARA container, used for logical
        # separation of services deploying the service engine
        self.container = container

        # actual engine class name
        self.engine_class_name = engine_class_name

        ServiceBase.object_pool_size = int(p_size)

        # Defines this service canonical name
        service_name = CUtility.form_canonical_name(xMsgUtil.get_local_ip(),
                                                    self.container,
                                                    self.engine_class_name)
        ServiceBase.__init__(self, service_name)

        # Create service executor objects and fill the pool
        for i in range(ServiceBase.object_pool_size):
            instance = ServiceExecutor(self.engine_class, self.container, self.engine_class_name)
            ServiceBase.available_object_pool.put(instance)

        # Dynamically loads service engine class
        engine_class = self._for_name(self.engine_class, self.engine_class_name)
        self.engine_object = engine_class()

        # Get description defined in the service engine
        self.description = self.engine_object.get_description()

        print "Registering with registration services..."

        # registration
        self.registerSubscriber(self.name,
                                xMsgUtil.get_local_ip(),
                                self.container,
                                self.engine_class_name,
                                self.description)

        # Subscribe messages addressed to this service container
        self.receive(self.name, self.call_back, False)

        xMsgUtil.keep_alive()

    def call_back(self, tr_data):
        """
        Service callback.
        This calls engine passing received data to it

        :param tr_data:
        """
        self.start_service(tr_data)

    def start_service(self, tr_object):

        composition = tr_object.composition

        # check to see if this is a configure request
        if tr_object.action == xMsgData_pb2.Data.CONFIGURE:

            # configure all engines in all service objects and return
            # Note: the successful configuration assumes that all
            #       objects are in the available pool.
            for i in range(ServiceBase.available_object_pool.qsize()):
                ins = ServiceBase.available_object_pool.get()
                ins.run(tr_object)
                ServiceBase.used_object_pool.put(ins)

            # return all objects to the pool of available objects
            for i in range(ServiceBase.used_object_pool.qsize()):
                ins = ServiceBase.used_object_pool.get()
                ServiceBase.available_object_pool.put(ins)
            return

        if tr_object.composition != self.p_composition:

            # This is new routing (composition)  request
            # clear local input-link dictionary and output-links list
            self.in_links.clear()

            # store it as previous
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

            else:
                self.in_links[tr_object.composition] = \
                    self.parse_in_linked(self.name, tr_object.composition)

        # define if this service has multiple inputs
        # and they are required to be logically ANDed
        log_and_request = self._is_log_and(self.name, composition)

        if log_and_request:

            # is the sender service is part of the input link schema
            if tr_object.sender in self.in_links.get(composition):

                # is this first time that service reporting?
                # if so create name map for this composition and
                # add the senders name to the list, mapped by
                # the composition string
                if composition not in self.dyn_in_name_list.keys():
                    x = [tr_object.sender]
                    ll = [tr_object]
                    self.dyn_in_name_list[composition] = x
                    self.dyn_in_data_list[composition] = ll
                    print "got the first request from sender = " + tr_object.sender

                # if composition exists add the senders name
                # to the list if not already added
                elif tr_object.sender not in self.dyn_in_name_list.get(composition):
                    self.dyn_in_name_list.get(composition).append(tr_object.sender)
                    self.dyn_in_data_list.get(composition).append(tr_object)
                    print "got the request from sender = " + tr_object.sender + " " +\
                          str(len(self.dyn_in_data_list.get(composition)))

                # check to see if all inputs for a logical AND are already sent data
                if len(self.dyn_in_name_list.get(composition)) == len(self.in_links.get(composition)):

                    # deep copy list of input data to this service
                    g_list = deepcopy(self.dyn_in_data_list.get(composition))

                    # get service object from the object pool and call
                    # execute method of that object in a separate thread
                    ins = self.get_object_from_pool()

                    print " Calling service executor = " + ins.name
                    # execute object method in a separate thread
                    t = threading.Thread(target=ins.run, args=g_list)
                    t.daemon = True
                    t.start()

                    # reset dynamic lists of composition specific lists
                    self.dyn_in_name_list.get(composition)[:] = []
                    self.dyn_in_data_list.get(composition)[:] = []

        else:
            # get service object from the object pool and call
            # execute method of that object in a separate thread
            l = [tr_object]
            ins = self.get_object_from_pool()
            # execute object method in a separate thread
            t = threading.Thread(target=ins.run, args=l)
            t.daemon = True
            t.start()


def main(engine_class, container, engine, object_pool_size):
    Service(engine_class, container, engine, object_pool_size)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
