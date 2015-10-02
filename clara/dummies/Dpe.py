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

import argparse
from xmsg.core.xMsg import xMsg
from xmsg.core.xMsgUtil import xMsgUtil
from xmsg.core.xMsgTopic import xMsgTopic
from xmsg.core.xMsgMessage import xMsgMessage
from xmsg.data import xMsgData_pb2
from xmsg.net.xMsgAddress import xMsgAddress
from clara.dummies.data.RuntimeDataGenerator import RuntimeDataGenerator
from clara.dummies.data.RegistrationDataGenerator import RegistrationDataGenerator


class StatsPublisher(xMsg):

    def __init__(self, host):
        super(StatsPublisher, self).__init__(host, "localhost",
                                             "localhost")
        self.connection = self.get_new_connection(xMsgAddress("localhost"))


class Dpe:
    '''Dummy Dpe just sending monitoring information.'''

    def __init__(self, host, n_containers, n_services):
        self.stats_publisher = StatsPublisher(host)
        self.host = host
        self.reg_data_generator = RegistrationDataGenerator(self.host,
                                                            n_containers,
                                                            n_services)
        self.run_data_generator = RuntimeDataGenerator(self.host,
                                                       n_containers,
                                                       n_services)

    def __make_name(self, suffix):
        return "%s:%s" % (self.host, suffix)

    def __send_message(self, topic, message):
        t_data = xMsgData_pb2.xMsgData()
        t_data.STRING = bytes(message)
        t_message = xMsgMessage(xMsgTopic.wrap(topic),
                                t_data.SerializeToString())
        self.stats_publisher.publish(self.stats_publisher.connection,
                                     t_message)

    def send_registration_data(self):
        """ Sends the DPE registration data in JSON format to the REST server"""
        xMsgUtil.log("dpe@%s : Publishing Registration Data..." % self.host)
        self.__send_message("registration_topic",
                            self.get_registration_data_json())

    def send_runtime_data(self):
        """ Sends the DPE runtime data in JSON format to the REST server"""
        xMsgUtil.log("dpe@%s : Publishing Runtime Data..." % self.host)
        self.__send_message("runtime_topic",
                            self.get_runtime_data_json())

    def get_registration_data_json(self):
        """ Gets the DPE registration data in JSON format

        Returns:
            JSON string
        """
        return self.reg_data_generator.get_data()

    def get_runtime_data_json(self):
        """ Gets the DPE runtime data in JSON format

        Returns:
            JSON string
        """
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
