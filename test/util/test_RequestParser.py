#
# Copyright (C) 2015. Jefferson Lab, CLARA framework (JLAB). All Rights Reserved.
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
from clara.util.RequestParser import RequestParser


class TestRequestParser(unittest.TestCase):

    def setUp(self):
        msg = "abc?cdr?33?some description"
        self.request = RequestParser(msg)

    def test_get_strings(self):
        first_string = self.request.next_string()
        second_integer = self.request.next_integer()
        third_string = self.request.next_string()
        fourth_string = self.request.next_string()

        self.assertIsInstance(first_string, basestring)
        self.assertIsInstance(second_integer, int)
        self.assertIsInstance(third_string, basestring)
        self.assertIsInstance(fourth_string, basestring)

        self.assertEqual(first_string, "some description")
        self.assertEqual(second_integer, 33)
        self.assertEqual(third_string, "cdr")
        self.assertEqual(fourth_string, "abc")

    def test_one_argument_request(self):
        msg = "STOP_DPE"
        request = RequestParser(msg)
        first_string = request.next_string()
        self.assertEqual(first_string, msg)

if __name__ == "__main__":
    unittest.main()
