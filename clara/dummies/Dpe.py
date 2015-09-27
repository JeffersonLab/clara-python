#!/usr/bin/env python
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
import json
import argparse
from datetime import datetime
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2, xMsgMeta_pb2
from xmsg.net.xMsgAddress import xMsgAddress


parser = argparse.ArgumentParser(description='Dummy DPE')
parser.add_argument('host', type=str,
                    help='ip of the dpe host')
args = parser.parse_args()


class StatsPublisher(xMsg):

    def __init__(self):
        super(StatsPublisher, self).__init__("dpe",
                                             "localhost",
                                             "localhost")
        self.connection = self.connect(xMsgAddress("localhost"))


class Dpe:
    '''
    Dummy Dpe just sending monitoring information.
    '''

    def __init__(self, host):
        self.stats_publisher = StatsPublisher()
        self.host = host

    def __make_name(self, suffix):
        return "%s:%s" % (self.host, suffix)

    def send_registration_data(self):
        print "Publishing Registration Data..."
        self.__send_message(self.get_registration_data_json())

    def send_runtime_data(self):
        print "Publishing Runtime Data..."
        self.__send_message(self.make_runtime_message())

    def __send_message(self, message):
        t_data = xMsgData_pb2.xMsgData()
        t_data.STRING = bytes(message)
        t_message = xMsgMessage(xMsgTopic.wrap("registration_topic"),
                                t_data.SerializeToString())
        self.stats_publisher.publish(self.stats_publisher.connection,
                                     t_message)

    def make_registration_message(self):
        """Gets the DPE registration data wrapped in xMsgMessage
        envelope

        Returns:
            xMsgMessage: message with DPE instant information
        """
        return self.__generate_message(self.get_registration_data_json())

    def make_runtime_message(self):
        """Gets the DPE runtime data wrapped in xMsgMessage
        envelope

        Method takes an snapshot of the current state of the DPE, and returns
        an xMsgMessage object.

        Returns:
            xMsgMessage: message with DPE instant information
        """
        return self.__generate_message(self.get_runtime_data_json())

    def __generate_message(self, json_data):
        data = xMsgData_pb2.xMsgData()
        data.STRING = json.dumps(json_data)
        msg = xMsgMessage.create_with_xmsg_data("registration_topic", data)
        meta_data = xMsgMeta_pb2.xMsgMeta()
        meta_data.dataType = "string"
        msg.set_metadata(meta_data)
        return msg

    def get_registration_data_json(self):
        """ Gets the DPE registration data in JSON format

        Returns:
            JSON string
        """
        # JSON keys
        d_key = "DPERegistration"
        c_key = "ContainerRegistration"
        s_key = "ServiceRegistration"
        fecha = datetime(2015, 9, 25, 11, 33, 21, 783116)

        dpe_json_data = {}
        dpe_json_data[d_key] = {}
        dpe_json_data[d_key]["host"] = self.host
        dpe_json_data[d_key]["n_cores"] = 8
        dpe_json_data[d_key]["memory_size"] = "64M"
        dpe_json_data[d_key]["language"] = "java"
        dpe_json_data[d_key]["start_time"] = str(fecha)
        dpe_json_data[d_key]["containers"] = []

        container_json_data = {}
        container_json_data[c_key] = {}
        container_json_data[c_key]["name"] = self.__make_name("cont_name")
        container_json_data[c_key]["language"] = "java"
        container_json_data[c_key]["author"] = "TEST DUMMY"
        container_json_data[c_key]["start_time"] = str(fecha)
        container_json_data[c_key]["services"] = []

        service_json_data = {}
        service_json_data[s_key] = {}
        service_json_data[s_key]["class_name"] = "SomeClassName"
        service_json_data[s_key]["engine_name"] = self.__make_name("cont_name:S1")
        service_json_data[s_key]["author"] = "Vardan"
        service_json_data[s_key]["version"] = "1.0"
        service_json_data[s_key]["description"] = "description of what i do"
        service_json_data[s_key]["language"] = "java"
        service_json_data[s_key]["start_time"] = str(fecha)

        container_json_data[c_key]["services"].append(service_json_data)
        dpe_json_data[d_key]["containers"].append(container_json_data)

        return dpe_json_data

    def get_runtime_data_json(self, variance=1):
        """ Gets the DPE runtime data in JSON format

        Returns:
            JSON string
        """
        # JSON keys
        d_key = "DPERuntime"
        c_key = "ContainerRuntime"
        s_key = "ServiceRuntime"

        dpe_json_data = {}
        dpe_json_data[d_key] = {}
        dpe_json_data[d_key]["host"] = self.host
        dpe_json_data[d_key]["snapshot_time"] = 112455111903
        dpe_json_data[d_key]["cpu_usage"] = 760
        dpe_json_data[d_key]["memory_usage"] = 63
        dpe_json_data[d_key]["load"] = 0.9
        dpe_json_data[d_key]["containers"] = []

        container_json_data = {}
        container_json_data[c_key] = {}
        container_json_data[c_key]["name"] = self.__make_name("cont_name")
        container_json_data[c_key]["snapshot_time"] = 11245590398
        container_json_data[c_key]["n_requests"] = 1000
        container_json_data[c_key]["services"] = []

        service_json_data = {}
        service_json_data[s_key] = {}
        service_json_data[s_key]["name"] = self.__make_name("cont_name:S1")
        service_json_data[s_key]["snapshot_time"] = 1954869020
        service_json_data[s_key]["n_requests"] = 1000
        service_json_data[s_key]["n_failures"] = 10
        service_json_data[s_key]["shm_reads"] = 1000
        service_json_data[s_key]["shm_writes"] = 1000
        service_json_data[s_key]["bytes_recv"] = 0
        service_json_data[s_key]["bytes_sent"] = 0
        service_json_data[s_key]["exec_time"] = 134235243543

        container_json_data[c_key]["services"].append(service_json_data)
        dpe_json_data[d_key]["containers"].append(container_json_data)

        return dpe_json_data


def main():
    if args.host:
        dpe = Dpe(args.host)
    else:
        dpe = Dpe("localhost")

    try:
        while True:
            dpe.send_registration_data()
            xMsgUtil.sleep(5)

    except KeyboardInterrupt:
        print "Exiting..."
        return

if __name__ == '__main__':
    main()
