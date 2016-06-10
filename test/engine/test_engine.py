#
# Copyright (C) 2015. Jefferson Lab, Clara framework (JLAB). All Rights Reserved.
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
from clara.engine.Engine import Engine


class GoodEngine(Engine):

    def configure(self, input_data):
        return input_data

    def execute(self, input_data):
        return input_data

    def execute_group(self, inputs):
        return inputs

    def get_input_data_types(self):
        pass

    def get_output_data_types(self):
        pass

    def get_states(self):
        return [u"state0", u"state1", u"state2"]

    def get_description(self):
        return u"Some description..."

    def get_version(self):
        return u"v1.0"

    def get_author(self):
        return u"Ricardo Oyarzun"

    def reset(self):
        pass

    def destroy(self):
        pass


class BadEngine(Engine):

    def configure(self, input_data):
        pass


class TestEngine(unittest.TestCase):

    def test_good_engine(self):
        good_engine = GoodEngine()
        self.assertIsInstance(good_engine, Engine)

    def test_bad_engine(self):
        self.assertRaises(TypeError, lambda: BadEngine())


if __name__ == "__main__":
    unittest.main()
