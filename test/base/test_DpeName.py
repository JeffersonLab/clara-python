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
from clara.name.DpeName import DpeName
from clara.base.ClaraAddress import ClaraAddress
from clara.base.ClaraLang import ClaraLang


class TestDpeName(unittest.TestCase):

    def test_dpe_name(self):
        dpe = DpeName("192.1.1.1", 7771, "python")
        self.assertIsInstance(dpe, DpeName)
        self.assertEqual(dpe.canonical_name(), "192.1.1.1_python")
        self.assertEqual(dpe.name(), dpe.canonical_name())
        self.assertEqual(str(ClaraLang.PYTHON), dpe.language())
        self.assertIsInstance(dpe.address(), ClaraAddress)

if __name__ == "__main__":
    unittest.main()
