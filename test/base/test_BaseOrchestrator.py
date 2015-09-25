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

from clara.base.BaseOrchestrator import BaseOrchestrator


class TestBaseOrchestrator(unittest.TestCase):

    def setUp(self):
        self.orchestrator = BaseOrchestrator("129.57.114.94")

    def test_constructor_creates_object_and_sets_proper_name(self):
        self.assertRegexpMatches(self.orchestrator.base.myname,
                                 "^orchestrator[\d]{1,4}:localhost$")
        self.assertIsInstance(self.orchestrator, BaseOrchestrator)
    
    def test_build_data(self):
        topic_data = "2:3:4"
        self.assertEqual(topic_data, self.orchestrator._build_data(1,2,3,4))
        
    def test_deploy_container_does_correctly_generic_send(self):
        self.orchestrator.deploy_container("129.57.114.94_python:thecontainer")
