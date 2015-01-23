from core.xMsg import xMsg
from core.xMsgConstants import xMsgConstants
from core.xMsgUtil import xMsgUtil
from net.xMsgAddress import xMsgAddress

__author__ = 'gurjyan'


class CBase(xMsg):
    """
    Base class for service as well as for orchestrator classes
    Clara service name convention - dpe_host:container:engine_name
    """
    name = xMsgConstants.UNDEFINED
    node_connection = xMsgConstants.UNDEFINED
    call_back = xMsgConstants.UNDEFINED

    def __init__(self, name, feHost=xMsgConstants.LOCALHOST):
        xMsg.__init__(self, feHost)
        self.name = name

        # Create a socket connections to the xMsg node
        address = xMsgAddress()
        self.node_connection = self.connect(address)

    @staticmethod
    def parse_out_linked(service_name, composition):
        """
        Parses composition field of the transient data
        and returns the list of services output linked
        to this service, i.e. that are getting output
        data of this service.

        :param composition: the string of the composition
        :return: list containing names of linked services
        """

        # List that contains names of all linked services
        out_list = []

        c_list = composition.split("+")

        comp_list = []
        for s in c_list:

            # remove  '&' from the service name
            # (e.g. 129.57.81.247:cont1:&Engine3 to 129.57.81.247:cont1:Engine3
            if "&" in s:
                n_list = s.split("&")
                s = ""
                for sl in n_list:
                    s = s + sl

            comp_list.append(s)

        for s in comp_list:

            # See if the string contains this service name, and record the index
            # Note: multiple services can send to a single service, like: s1,s2+s3.
            # (this is the reason we use in:contains)
            #
            if service_name in s:
                index = comp_list.index(s)
                # index of the next component in the composition
                index += 1
                if len(comp_list) > index:
                    temp = comp_list[index]
                    if not "," in temp:
                        next_service_name = comp_list[index]
                        out_list.append(next_service_name)
                    else:

                        # this is a case where output of this service goes to many services
                        s_temp = temp.split(",")
                        for m in s_temp:
                            out_list.append(m)
                break

        return out_list

    @staticmethod
    def parse_in_linked(service_name, composition):
        """
        Parses "composition" field of the transient data
        and returns the list of services that are
        input-linked to send data to this service.

        :param composition: the string of the composition
        :return: list containing names of linked services
        """

        # List that contains names of all linked services
        out_list = []

        index = 0
        comp_list = composition.split("+")
        for s in comp_list:

            # See if the string contains this service name, and record the index
            # Note: multiple services can send to a single service, like: s1,s2+s3.
            # (this is the reason we use in:contains)
            #
            if service_name in s:
                index = comp_list.index(s)
                break

        # index of the previous component in the composition
        index -= 1
        if index >= 0:
            temp = comp_list[index]
            if not "," in temp:
                previous_service_name = comp_list[index]
                out_list.append(previous_service_name)
            else:

                # this is a case where output of many services
                # goes to the input of this service
                s_temp = temp.split(",")
                for m in s_temp:
                    out_list.append(m)
        return out_list

    @staticmethod
    def _is_log_and(service_name, composition):
        """
        Check to see in the composition this service
        is required to logically AND inputs before
        executing its service

        :param composition: The string of the composition
        :return: True if component name is programmed
                 as "&<service_name>"
        """
        ac = "&" + service_name
        comp_list = composition.split("+")

        for s in comp_list:
            if ac in s:
                return True
        return False

    def find_service(self, service_name):
        """
         Sends a request to the xMsg registration service,
         asking to return registration information of service/services
         based on dpe_host, container and engine names.
         Note that character * can be used for any/all container and
         engine names. * is not permitted for dpe_host specification

        :param service_name: service canonical name
        :return: set of xMsgRegistrationData objects
        """
        if xMsgUtil.get_domain(service_name) is xMsgConstants.ANY:
            raise Exception("Host name of the DPE must be specified")
        else:
            if xMsgUtil.get_domain(service_name) == xMsgUtil.get_local_ip():
                return self.findLocalSubscriber(self.name,
                                                xMsgUtil.get_domain(service_name),
                                                xMsgUtil.get_subject(service_name),
                                                xMsgUtil.get_type(service_name))
            else:
                return self.findSubscriber(self.name,
                                           xMsgUtil.get_domain(service_name),
                                           xMsgUtil.get_subject(service_name),
                                           xMsgUtil.get_type(service_name),
                                           xMsgUtil.get_domain(service_name))

    def receive(self, topic, call_back, is_sync=True):

        """
        This method simply calls xMsg subscribe method
        passing the reference to user provided call_back method.

        :param topic: Service canonical name that this
                             method will subscribe or listen
        :param call_back: User provided call_back function.
        :param is_sync:
        """
        self.subscribe(self.node_connection,
                       xMsgUtil.get_domain(topic),
                       xMsgUtil.get_subject(topic),
                       xMsgUtil.get_type(topic),
                       call_back,
                       is_sync)

    def receive_new(self, connection, topic, call_back, is_sync=True):

        """
        This method simply calls xMsg subscribe method
        passing the reference to user provided call_back method.
        The only difference is that this method requires a
        connection socket different than the default socket connection
        to the local dpe proxy.

        :param connection object
        :param topic: Service canonical name that this
                             method will subscribe or listen
        :param call_back: User provided call_back function.
        :param is_sync:
        """
        self.subscribe(connection,
                       xMsgUtil.get_domain(topic),
                       xMsgUtil.get_subject(topic),
                       xMsgUtil.get_type(topic),
                       call_back,
                       is_sync)

    def send(self, topic, data):
        """
        Sends xMsgData object to a service defined by:

        :param topic: Clara service canonical name where
                      the data will be sent as an input
        :param data: xMsgData object
        """
        self.publish(self.node_connection,
                     xMsgUtil.get_domain(topic),
                     xMsgUtil.get_subject(topic),
                     xMsgUtil.get_type(topic),
                     self.name,
                     data)

    def send_new(self, connection, topic, data):
        """
        Sends xMsgData object to a service defined by:

        :param connection: connection socket
        :param topic: Clara service canonical name where
                      the data will be sent as an input
        :param data: xMsgData object
        """
        self.publish(connection,
                     xMsgUtil.get_domain(topic),
                     xMsgUtil.get_subject(topic),
                     xMsgUtil.get_type(topic),
                     self.name,
                     data)
