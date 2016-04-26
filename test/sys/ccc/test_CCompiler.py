# coding=utf-8

import unittest

from ordered_set import OrderedSet

from clara.base.error.ClaraException import ClaraException
from clara.sys.ccc.CCompiler import CCompiler
from clara.sys.ccc.ServiceState import ServiceState


class TestCCompiler(unittest.TestCase):

    @staticmethod
    def get_composition():
        return "10.10.10.1_java:C:S1+10.10.10.1_java:C:S2+" +\
               "10.10.10.1_java:C:S3+10.10.10.1_java:C:S4;"

    def test_catch_missing_statement_with_exception(self):
        with self.assertRaises(ClaraException):
            cc = CCompiler("10.10.10.1_java:C:S5")
            cc.compile(TestCCompiler.get_composition())

    def test_service_at_the_middle(self):
        cc = CCompiler("10.10.10.1_java:C:S3")
        cc.compile(TestCCompiler.get_composition())
        self.assertEqual(set(["10.10.10.1_java:C:S4"]),
                         cc.get_unconditional_links())

    def test_service_at_the_end(self):
        cc = CCompiler("10.10.10.1_java:C:S4")
        cc.compile(TestCCompiler.get_composition())
        self.assertEqual(set([]), cc.get_unconditional_links())

    def test_service_at_the_beginning(self):
        cc = CCompiler("10.10.10.1_java:C:S1")
        cc.compile(TestCCompiler.get_composition())
        self.assertEqual(set(["10.10.10.1_java:C:S2"]),
                         cc.get_unconditional_links())

    def test_service_on_a_loop(self):
        composition = "10.10.10.1_java:C:S1+10.10.10.1_java:C:S2+" +\
                      "10.10.10.1_java:C:S1;"
        cc = CCompiler("10.10.10.1_java:C:S2")
        cc.compile(composition)
        self.assertEqual(set(["10.10.10.1_java:C:S1"]),
                         cc.get_unconditional_links())

    def test_on_multiple_call(self):
        composition_extra = "10.10.10.1_java:C:S1+10.10.10.1_java:C:S2+" + \
                            "10.10.10.1_java:C:S1;"

        cc = CCompiler("10.10.10.1_java:C:S2")
        cc.compile(TestCCompiler.get_composition())
        cc.compile(composition_extra)
        self.assertEqual(set(["10.10.10.1_java:C:S1"]),
                         cc.get_unconditional_links())

    def test_conditional(self):
        cc = CCompiler("10.10.10.1_java:C:S1")
        cc.compile(TestCCompiler.get_composition())
        composition2 = "10.10.10.1_java:C:S1;" +\
                       "if (10.10.10.1_java:C:S1 == \"FOO\") { " +\
                       "  10.10.10.1_java:C:S1+10.10.10.1_java:C:S2;" +\
                       "}"
        cc.compile(composition2)
        owner_ss = ServiceState("10.10.10.1_java:C:S1", "\"FOO\"")
        input_ss = ServiceState("WHATEVER", "DON'T CARE")
        self.assertEqual(OrderedSet(["10.10.10.1_java:C:S2"]),
                         cc.get_links(owner_ss, input_ss))

    def test_elif_conditional(self):
        cc = CCompiler("10.10.10.1_java:C:S1")
        cc.compile(TestCCompiler.get_composition())
        composition2 = "10.10.10.1_java:C:S1;" +\
                       "if (10.10.10.1_java:C:S1 == \"FOO\") { " +\
                       "  10.10.10.1_java:C:S1+10.10.10.1_java:C:S2;" +\
                       "} elseif (10.10.10.1_java:C:S1 == \"BAR\") { " +\
                       "  10.10.10.1_java:C:S1+10.10.10.1_java:C:S3;" +\
                       "} elseif (10.10.10.1_java:C:S1 == \"FROZ\") { " +\
                       "  10.10.10.1_java:C:S1+10.10.10.1_java:C:S4;" +\
                       "}"
        cc.compile(composition2)
        owner_ss = ServiceState("10.10.10.1_java:C:S1", "\"FROZ\"")
        input_ss = ServiceState("WHATEVER", "DON'T CARE")
        self.assertEqual(OrderedSet(["10.10.10.1_java:C:S4"]),
                         cc.get_links(owner_ss, input_ss))


if __name__ == "__main__":
    unittest.main()
