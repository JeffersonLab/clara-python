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
from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraRequest import DeployContainerRequest, DeployServiceRequest
from clara.name.ContainerName import ContainerName
from clara.name.ServiceName import ServiceName
from clara.name.DpeName import DpeName



class TestClaraRequest(unittest.TestCase):

    def setUp(self):
        self.dpe = DpeName("localhost", 7771, "python")

    def test_deploy_container_request_constructor(self):
        frontend = ""
        container = ContainerName(self.dpe, "asdf")
        base = ClaraBase("myname", "localhost", "localhost", 7771, 8888)
        deploy_container_req = DeployContainerRequest(base, frontend,
                                                      container)
        self.assertIsInstance(deploy_container_req, DeployContainerRequest)

    def test_deploy_service_request_constructor(self):
        frontend = ""
        container = ContainerName(self.dpe, "asdf")
        service = ServiceName(container, "foobar")
        base = ClaraBase("myname", "localhost", "localhost", 7771, 8888)
        deploy_service_req = DeployServiceRequest(base, frontend, service,
                                                  "class_path")
        self.assertIsInstance(deploy_service_req, DeployServiceRequest)

if __name__ == "__main__":
    unittest.main()
