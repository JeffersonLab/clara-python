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

import unittest
import re

from clara.base.ClaraUtils import ClaraUtils
from clara.base.ClaraLang import ClaraLang
from xmsg.core.xMsgConstants import xMsgConstants

CONTAINER_VALID_CASES = ["10.2.58.17_java:master",
                         "10.2.58.17_java:best_container",
                         "10.2.58.17_cpp:container1",
                         "10.2.58.17_python:User",
                         "10.2.58.17_java:master",
                         "10.2.58.17_java:best_container",
                         "10.2.58.17_cpp:container1",
                         "10.2.58.17_python:User",
                         ]

CONTAINER_INVALID_CASES = ["129.57.28.27_java:master:Simple:Engine",
                           "10.2.58.17_java:master:some_service",
                           "10.2.58.17_javax::master",
                           "10.2.58.17_javax::master",
                           "10.2.58.17_java::best_container",
                           "10.2.58.17_cpp::container1:",
                           "10.2.58.17_cpp:container1:",
                           "10.2.58.17_python:User::",
                           "10.2.58.17_java:master**",
                           "10.2.58.17_java",
                           ]

DPE_VALID_CASES = ["10.2.58.17_java",
                   "10.2.58.17_cpp",
                   "10.2.58.17_python",
                   "10.2.58.17_java",
                   "10.2.58.17_java",
                   "10.2.58.17_cpp",
                   "10.2.58.17_python",
                   ]

DPE_INVALID_CASES = ["10.2.58.17 _java",
                     "10.2.58.17_cppx",
                     "10.2.58.17-python",
                     "10.2.58.17_java8",
                     "10.2.58.17_ cpp",
                     "10.2.58.17 _ python",
                     ]

SERVICE_VALID_CASES = ["129.57.28.27_java:master:SimpleEngine",
                       "129.57.28.27_cpp:container1:IntegrationEngine",
                       "129.57.28.27_python:User:StatEngine",
                       ]

SERVICE_INVALID_CASES = ["129.57.28.27_java",
                         "129.57.28.27_java:master",
                         "129.57.28.27_java:master:Simple:Engine",
                         "129.57.28.27_cpp:container1:Integration...",
                         "129.57.28.27_python:User:Stat,Engine",
                         ]

NAME_VALID_CASES = ["dpe_java:c:s",
                    "dpe_java:c",
                    ]


class TestClaraUtils(unittest.TestCase):

    def test_is_dpe_pos(self):
        for case in DPE_VALID_CASES:
            test_case = ClaraUtils.is_dpe_name(case)
            self.assertTrue(test_case)

    def test_is_dpe_neg(self):
        for case in DPE_INVALID_CASES:
            test_case = ClaraUtils.is_dpe_name(case)
            self.assertFalse(test_case)

    def test_is_container_pos(self):
        for case in CONTAINER_VALID_CASES:
            test_case = ClaraUtils.is_container_name(case)
            self.assertTrue(test_case)

    def test_is_container_neg(self):
        for case in CONTAINER_INVALID_CASES:
            test_case = ClaraUtils.is_container_name(case)
            self.assertFalse(test_case)

    def test_is_service_name_pos(self):
        for case in SERVICE_VALID_CASES:
            test_case = ClaraUtils.is_service_name(case)
            self.assertTrue(test_case)

    def test_is_service_name_neg(self):
        for case in SERVICE_INVALID_CASES:
            test_case = ClaraUtils.is_service_name(case)
            self.assertFalse(test_case)

    def test_get_hostname(self):
        for case in SERVICE_VALID_CASES:
            test_case = ClaraUtils.get_hostname(case)
            self.assertEqual(test_case, "129.57.28.27")

    def test_is_dpe_name(self):
        for case in DPE_VALID_CASES:
            regex_validation = re.compile("^([^:_ ]+_(java|python|cpp))")
            self.assertTrue(ClaraUtils.is_dpe_name(case))
            self.assertIsNotNone(regex_validation.match(case))

    def test_get_container_name(self):
        for case in NAME_VALID_CASES:
            test_case = ClaraUtils.get_container_name(case)
            self.assertEqual(test_case, "c")

    def test_get_container_canonical_name(self):
        for case in NAME_VALID_CASES:
            test_case = ClaraUtils.get_container_canonical_name(case)
            self.assertEqual(test_case, "dpe_java:c")

    def test_form_dpe_name(self):
        test_case = ClaraUtils.form_dpe_name("192.168.0.1", ClaraLang.JAVA)
        self.assertTrue(ClaraUtils.is_dpe_name(test_case))
        self.assertEqual(test_case, "192.168.0.1_java")
        test_case = ClaraUtils.form_dpe_name("192.168.0.1", ClaraLang.JAVA, 8181)
        self.assertTrue(ClaraUtils.is_dpe_name(test_case))
        self.assertEqual(test_case, "192.168.0.1%8181_java")

    def test_form_container_name(self):
        test_case = ClaraUtils.form_dpe_name("192.168.0.1", ClaraLang.JAVA)
        self.assertTrue(ClaraUtils.is_dpe_name(test_case))
        self.assertEqual(test_case, "192.168.0.1_java")

    def test_form_service_name(self):
        test_case = ClaraUtils.form_service_name("192.168.0.1_java:some_container",
                                                 "some_engine")
        self.assertTrue(ClaraUtils.is_service_name(test_case))
        self.assertEqual(test_case,
                         "192.168.0.1_java:some_container:some_engine")

    def test_get_cpu_usage(self):
        test_case = ClaraUtils.get_cpu_usage()
        self.assertIsInstance(test_case, float)
        self.assertGreater(test_case, 0.0)

    def test_get_mem_usage(self):
        test_case = ClaraUtils.get_mem_usage()
        self.assertIsInstance(test_case, float)
        self.assertGreater(test_case, 0.0)

    def test_compose_canonical_name(self):
        test1 = "192.168.0.1_java:some_container:some_engine"
        test_case = ClaraUtils.decompose_canonical_name(test1)
        expected1 = ["192.168.0.1", int(xMsgConstants.DEFAULT_PORT),
                     "java", "some_container", "some_engine"]
        self.assertEqual(test_case, expected1)

        test2 = "192.168.0.1%2222_java:some_container:some_engine"
        test_case = ClaraUtils.decompose_canonical_name(test2)
        expected2 = ["192.168.0.1", 2222,
                     "java", "some_container", "some_engine"]
        self.assertEqual(test_case, expected2)

if __name__ == "__main__":
    unittest.main()
