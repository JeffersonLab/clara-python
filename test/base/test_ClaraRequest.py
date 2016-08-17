# coding=utf-8

import unittest
from clara.base.ClaraBase import ClaraBase
from clara.base.ClaraNames import DpeName, ContainerName, ServiceName
from clara.base.ClaraRequest import DeployContainerRequest, DeployServiceRequest


class TestClaraRequest(unittest.TestCase):

    def setUp(self):
        self.dpe = DpeName("localhost", 7771, "python")

    def test_deploy_container_request_constructor(self):
        frontend = ""
        container = ContainerName(self.dpe, "asdf")
        base = ClaraBase("myname", "localhost",  7771, "localhost", 8888)
        deploy_container_req = DeployContainerRequest(base, frontend,
                                                      container)
        self.assertIsInstance(deploy_container_req, DeployContainerRequest)

    def test_deploy_service_request_constructor(self):
        frontend = ""
        container = ContainerName(self.dpe, "asdf")
        service = ServiceName(container, "foobar")
        base = ClaraBase("myname", "localhost", 7771, "localhost",8888)
        deploy_service_req = DeployServiceRequest(base, frontend, service,
                                                  "class_path")
        self.assertIsInstance(deploy_service_req, DeployServiceRequest)

if __name__ == "__main__":
    unittest.main()
