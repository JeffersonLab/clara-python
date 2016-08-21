# coding=utf-8

import unittest
from clara.util.RequestParser import RequestParser


class TestRequestParser(unittest.TestCase):

    def setUp(self):
        msg = "abc?cdr?33?some description"
        self.request = RequestParser(msg)

    def test_get_strings(self):
        first_string = self.request.next_string()
        second_string = self.request.next_string()
        third_integer = self.request.next_integer()
        fourth_string = self.request.next_string()

        self.assertIsInstance(first_string, basestring)
        self.assertIsInstance(second_string, basestring)
        self.assertIsInstance(third_integer, int)
        self.assertIsInstance(fourth_string, basestring)

        self.assertEqual(first_string, "abc")
        self.assertEqual(second_string, "cdr")
        self.assertEqual(third_integer, 33)
        self.assertEqual(fourth_string, "some description")

    def test_one_argument_request(self):
        msg = "STOP_DPE"
        request = RequestParser(msg)
        first_string = request.next_string()
        self.assertEqual(first_string, msg)

if __name__ == "__main__":
    unittest.main()
