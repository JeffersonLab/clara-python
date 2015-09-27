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
from datetime import datetime
from xmsg.core.xMsgMessage import xMsgMessage

from clara.dummies.Dpe import Dpe

fecha = str(datetime(2015, 9, 25, 11, 33, 21, 783116))

TEST_CASE_1 = {
  "DPERegistration": {
    "language": "java",
    "start_time": fecha,
    "n_cores": 8,
    "host": "localhost",
    "memory_size": "64M",
    "containers": [
      {
        "ContainerRegistration": {
          "name": "localhost:cont_name",
          "language": "java",
          "author": "TEST DUMMY",
          "start_time": fecha,
          "services": [
            {
              "ServiceRegistration": {
                "description": "description of what i do",
                "language": "java",
                "author": "Vardan",
                "class_name": "SomeClassName",
                "version": "1.0",
                "start_time": fecha,
                "engine_name": "localhost:cont_name:S1"
              }
            }
          ],
        }
      }
    ]
  }
}

TEST_CASE_2 = {
  "DPERuntime": {
    "host": "localhost",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
         "ContainerRuntime": {
            "name": "localhost:cont_name",
            "snapshot_time": 11245590398,
            "n_requests": 1000,
            "services": [
              {
                "ServiceRuntime": {
                  "name": "localhost:cont_name:S1",
                  "snapshot_time": 1954869020,
                  "n_requests": 1000,
                  "n_failures": 10,
                  "shm_reads": 1000,
                  "shm_writes": 1000,
                  "bytes_recv": 0,
                  "bytes_sent": 0,
                  "exec_time": 134235243543
                }
              }
            ]
          }
      }
    ]
  }
}

TEST_CASE_3 = {
  "DPERegistration": {
    "language": "java",
    "start_time": fecha,
    "n_cores": 8,
    "host": "192.168.1.1",
    "memory_size": "64M",
    "containers": [
      {
        "ContainerRegistration": {
          "name": "192.168.1.1:cont_name",
          "language": "java",
          "author": "TEST DUMMY",
          "start_time": fecha,
          "services": [
            {
              "ServiceRegistration": {
                "description": "description of what i do",
                "language": "java",
                "author": "Vardan",
                "class_name": "SomeClassName",
                "version": "1.0",
                "start_time": fecha,
                "engine_name": "192.168.1.1:cont_name:S1"
              }
            }
          ],
        }
      }
    ]
  }
}

TEST_CASE_4 = {
  "DPERuntime": {
    "host": "192.168.1.1",
    "snapshot_time": 112455111903,
    "cpu_usage": 760,
    "memory_usage": 63,
    "load": 0.9,
    "containers": [
      {
         "ContainerRuntime": {
            "name": "192.168.1.1:cont_name",
            "snapshot_time": 11245590398,
            "n_requests": 1000,
            "services": [
              {
                "ServiceRuntime": {
                  "name": "192.168.1.1:cont_name:S1",
                  "snapshot_time": 1954869020,
                  "n_requests": 1000,
                  "n_failures": 10,
                  "shm_reads": 1000,
                  "shm_writes": 1000,
                  "bytes_recv": 0,
                  "bytes_sent": 0,
                  "exec_time": 134235243543
                }
              }
            ]
          }
      }
    ]
  }
}


class TestDummyDPE(unittest.TestCase):

    def setUp(self):
        self.dpe_0 = Dpe("localhost")
        self.dpe_1 = Dpe("192.168.1.1")

    def test_get_registration_data_json(self):
        self.assertEqual(TEST_CASE_1, self.dpe_0.get_registration_data_json())
        self.assertEqual(TEST_CASE_3, self.dpe_1.get_registration_data_json())

    def test_get_registration_message(self):
        self.assertIsInstance(self.dpe_0.make_registration_message(),
                              xMsgMessage)
        self.assertIsInstance(self.dpe_1.make_registration_message(),
                              xMsgMessage)

    def test_get_runtime_data_json(self):
        self.assertEqual(TEST_CASE_2, self.dpe_0.get_runtime_data_json())
        self.assertEqual(TEST_CASE_4, self.dpe_1.get_runtime_data_json())

    def test_get_runtime_message(self):
        self.assertIsInstance(self.dpe_0.make_runtime_message(), xMsgMessage)
        self.assertIsInstance(self.dpe_1.make_runtime_message(), xMsgMessage)


if __name__ == "__main__":
    unittest.main()
