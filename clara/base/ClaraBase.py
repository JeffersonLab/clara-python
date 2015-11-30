#
# Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Vardan Gyurjyan
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

from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.net.xMsgAddress import RegAddress, ProxyAddress

from clara.util.CUtility import CUtility


class CBase(xMsg):
    """Base class for service and orchestrator classes as well

    Clara service name convention - dpe-host_lang:container:engine_name
    """
    name = str(xMsgConstants.UNDEFINED)
    node_connection = str(xMsgConstants.UNDEFINED)
    call_back = str(xMsgConstants.UNDEFINED)

    def __init__(self, name, proxy_address=ProxyAddress(),
                 reg_address=RegAddress()):
        super(CBase, self).__init__(name, proxy_address, reg_address)

        # Create a socket connections to the xMsg node
        self.node_connection = self.connect(proxy_address)

    @staticmethod
    def parse_out_linked(service_name, composition):
        """Parses composition field of the transient data

        returns the list of services output linked to this service, i.e. that
        are getting output data of this service.

        Args:
            composition (String): the string of the composition

        Returns:
            list containing names of linked services
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

            # See if the string contains this service name, and record the
            # index
            # Note: multiple services can send to a single service, like:
            # s1,s2+s3. (this is the reason we use in:contains)
            #
            if service_name in s:
                index = comp_list.index(s)
                # index of the next component in the composition
                index += 1
                if len(comp_list) > index:
                    temp = comp_list[index]
                    if "," in temp:
                        # this is a case where output of this service goes to
                        # many services
                        s_temp = temp.split(",")
                        out_list = [m for m in s_temp]
                    else:
                        next_service_name = comp_list[index]
                        out_list.append(next_service_name)

                break

        return out_list

    @staticmethod
    def parse_in_linked(service_name, composition):
        """xParses "composition" field of the transient data and returns the list
        of services that are input-linked to send data to this service.

        Args:
            composition (String): the string of the composition
        Returns:
            list containing names of linked services
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
            if "," in temp:
                # this is a case where output of many services
                # goes to the input of this service
                s_temp = temp.split(",")
                for m in s_temp:
                    out_list.append(m)
            else:
                previous_service_name = comp_list[index]
                out_list.append(previous_service_name)
        return out_list

    @staticmethod
    def _is_it_logical_and(service_name, composition):
        """Check to see in the composition this service is required to
        logically AND inputs before executing its service

        Args:
            composition (String): The string of the composition

        Returns:
            boolean: True if component name is programmed
                as "&<service_name>"
        """
        ac = "&" + service_name
        # comp_list = composition.split("+")

        for s in composition.split("+"):
            if ac in s:
                return True

        return False

    def register(self, description=str(xMsgConstants.UNDEFINED)):
        self.register_as_subscriber(self.name, description)

    def find_service(self, service_name):
        """Sends a request to the xMsg registration service,

        asking to return registration information of service/services based on
        dpe_host, container and engine names.
        Note that character * can be used for any/all container and engine
        names * is not permitted for dpe_host specification

        Args:
            service_name (xMsgTopic): service canonical name

        Returns:
            Set: set of xMsgRegistration objects
        """
        if service_name.domain == str(xMsgConstants.ANY):
            raise Exception("Host name of the DPE must be specified")

        else:
            if service_name.domain == xMsgUtil.get_local_ip():
                return self.find_local_subscriber(service_name)

            else:
                return self.find_subscriber(service_name)

    def listen(self, topic, callback):
        """This method simply calls xMsg subscribe method passing the reference to
        user provided call_back method.

        Args:
            topic (xMsgTopic): Topic of subscription
            call_back (xMsgCallBack): User provided call_back object
        """
        self.subscribe(topic, self.node_connection, callback)

    def send(self, msg):
        """Sends xMsgMessage object to an xMsg actor

        Args:
            msg (xMsgMessage): xMsg transient message object
        """
        self.publish(self.node_connection, msg)

    def sync_send(self, msg):
        """Sends xMsgMessage object to an xMsg actor synchronously

        Args:
            msg (xMsgMessage): xMsg transient message object
        """
        self.sync_publish(self.node_connection, msg, 30)

