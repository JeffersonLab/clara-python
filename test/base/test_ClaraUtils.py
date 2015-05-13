'''
Created on 12-05-2015

@author: royarzun
'''
import unittest
import re
from src.base.ClaraUtils import ClaraUtils
from src.base.ClaraLang import ClaraLang

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

    def test_isDpe_pos(self):
        for case in DPE_VALID_CASES:
            test_case = ClaraUtils.isDpeName(case)
            self.assertEqual(test_case, True)

    def test_isDpe_neg(self):
        for case in DPE_INVALID_CASES:
            test_case = ClaraUtils.isDpeName(case)
            print case
            self.assertEqual(test_case, False)

    def test_isContainer_pos(self):
        for case in CONTAINER_VALID_CASES:
            test_case = ClaraUtils.isContainerName(case)
            self.assertEqual(test_case, True)

    def test_isContainer_neg(self):
        for case in CONTAINER_INVALID_CASES:
            test_case = ClaraUtils.isContainerName(case)
            self.assertEqual(test_case, False)

    def test_isServiceName_pos(self):
        for case in SERVICE_VALID_CASES:
            test_case = ClaraUtils.isServiceName(case)
            self.assertEqual(test_case, True)

    def test_isServiceName_neg(self):
        for case in SERVICE_INVALID_CASES:
            test_case = ClaraUtils.isServiceName(case)
            self.assertEqual(test_case, False)
    
    def test_get_hostname(self):
        for case in SERVICE_VALID_CASES:
            test_case = ClaraUtils.getHostname(case)
            self.assertEqual(test_case, "129.57.28.27")
    
    def test_isDpeName(self):
        for case in DPE_VALID_CASES:
            test_case = ClaraUtils.isDpeName(case)
            regex_validation = re.compile("^([^:_ ]+_(java|python|cpp))")
            self.assertIsNot(regex_validation.match(case), None)
            
    def test_getContainerName(self):        
        for case in NAME_VALID_CASES:
            test_case = ClaraUtils.getContainerName(case)
            self.assertEqual(test_case, "c")
    
    def test_getContainerCanonicalName(self):
        for case in NAME_VALID_CASES:
            test_case = ClaraUtils.getContainerCanonicalName(case)            
            self.assertEqual(test_case, "dpe_java:c")
            
    def test_formDpeName(self):
        test_case = ClaraUtils.formDpeName("192.168.0.1", ClaraLang.JAVA)
        print test_case
        self.assertEqual(ClaraUtils.isDpeName(test_case), True)
        self.assertEqual(test_case, "192.168.0.1_java")
    
    def test_form_container_name(self):
        test_case = ClaraUtils.formDpeName("192.168.0.1", ClaraLang.JAVA)
        self.assertEqual(ClaraUtils.isDpeName(test_case), True)
        self.assertEqual(test_case, "192.168.0.1_java")
    
    def test_formServiceName(self):
        test_case = ClaraUtils.formServiceName("192.168.0.1_java:some_container",
                                                 "some_engine")
        self.assertEqual(ClaraUtils.isServiceName(test_case), True)
        self.assertEqual(test_case, "192.168.0.1_java:some_container:some_engine")

if __name__ == "__main__":
    unittest.main()
