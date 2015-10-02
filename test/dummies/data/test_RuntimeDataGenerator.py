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
import unittest
from clara.dummies.data.RuntimeDataGenerator import RuntimeDataGenerator


class TestRuntimeDataGenerator(unittest.TestCase):

    def test_constructor(self):
        r_data = RuntimeDataGenerator("1.1.1.1", 1, 1)
        self.assertTrue("DPERuntime" in r_data.get_data())

    def test_create_with_two_containers(self):
        r_data = RuntimeDataGenerator("1.1.1.1", 2, 0)
        self.assertEqual(len(json.loads(r_data.get_data())['DPERuntime']['containers']), 2)

    def test_create_with_two_containers_with_two_services(self):
        r_data = RuntimeDataGenerator("1.1.1.1", 2, 2)
        self.assertEqual(len(json.loads(r_data.get_data())['DPERuntime']['containers']), 2)
        for container in json.loads(r_data.get_data())['DPERuntime']['containers']:
            self.assertEqual(len(container['ContainerRuntime']['services']), 2)

    def test_get_data_called_twice_modifies_stored_data(self):
        r_data = RuntimeDataGenerator("1.1.1.1", 10, 21)
        first_call = r_data.get_data()
        self.assertNotEqual(first_call, r_data.get_data())

if __name__ == "__main__":
    unittest.main()
