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

import simplejson as json
import argparse
from datetime import datetime
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2
from xmsg.net.xMsgAddress import xMsgAddress
from clara.dummies.data.RuntimeDataGenerator import RuntimeDataGenerator


class StatsPublisher(xMsg):

    def __init__(self):
        super(StatsPublisher, self).__init__("dpe",
                                             "localhost",
                                             "localhost")
        self.connection = self.get_new_connection(xMsgAddress("localhost"))


class Dpe:
    '''Dummy Dpe just sending monitoring information.'''

    def __init__(self, host, n_containers, n_services):
        self.stats_publisher = StatsPublisher()
        self.host = host
        self.run_data_generator = RuntimeDataGenerator("regData",
                                                       n_containers,
                                                       n_services)

    def __make_name(self, suffix):
        return "%s:%s" % (self.host, suffix)

    def send_registration_data(self):
        xMsgUtil.log("dpe@%s : Publishing Registration Data..." % self.host)
        self.__send_message("registration_topic", self.get_registration_data_json())

    def send_runtime_data(self):
        xMsgUtil.log("dpe@%s : Publishing Runtime Data..." % self.host)
        self.__send_message("runtime_topic", self.get_runtime_data_json())

    def __send_message(self, topic, message):
        t_data = xMsgData_pb2.xMsgData()
        t_data.STRING = bytes(message)
        t_message = xMsgMessage(xMsgTopic.wrap(topic),
                                t_data.SerializeToString())
        self.stats_publisher.publish(self.stats_publisher.connection,
                                     t_message)

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
        dpe_json_data[d_key]["hostname"] = self.host
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

        return json.dumps(dpe_json_data, sort_keys=True)

    def get_runtime_data_json(self):
        return self.run_data_generator.get_data()


def main():
    dpe = Dpe(args.host, args.n_containers, args.n_services)

    try:
        while True:
            dpe.send_registration_data()
            dpe.send_runtime_data()
            xMsgUtil.sleep(5)

    except KeyboardInterrupt:
        print "Exiting..."
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dummy DPE')
    parser.add_argument('host', type=str, help='ip of the dpe host')
    parser.add_argument('n_containers', type=int, help='n containers in DPE')
    parser.add_argument('n_services', type=int, help='n services in container')
    args = parser.parse_args()
    main()
