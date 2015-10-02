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

import unittest
import simplejson as json
from xmsg.core.xMsgMessage import xMsgMessage
from clara.dummies.Dpe import Dpe


class TestDummyDPE(unittest.TestCase):

    def setUp(self):
        self.dpe_0 = Dpe("localhost", 1, 1)
        self.dpe_1 = Dpe("192.168.1.1", 1, 1)

    def test_get_registration_data_json(self):
        self.assertTrue("DPERegistration" in json.loads(self.dpe_0.get_registration_data_json()))
        self.assertTrue("DPERegistration" in json.loads(self.dpe_1.get_registration_data_json()))

    def test_get_runtime_data_json(self):
        self.assertTrue("DPERuntime" in json.loads(self.dpe_0.get_runtime_data_json()))
        self.assertTrue("DPERuntime" in json.loads(self.dpe_1.get_runtime_data_json()))
        
    def test_create_2_2_dpe(self):
        dpe = Dpe("localhost", 2, 2)
        containers = json.loads(dpe.get_runtime_data_json())['DPERuntime']['containers']
        services = containers[0]['ContainerRuntime']['services']
        self.assertEqual(len(containers), 2)
        self.assertEqual(len(services), 2)


if __name__ == "__main__":
    unittest.main()
