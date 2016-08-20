# coding=utf-8

import unittest
from mockito import mock, verify, any
from xmsg.core.xMsgConstants import xMsgConstants
from xmsg.core.xMsgMessage import xMsgMessage

from clara.base.BaseOrchestrator import BaseOrchestrator
from clara.base.ClaraBase import ClaraBase


class TestBaseOrchestrator(unittest.TestCase):

    def setUp(self):
        self.orchestrator = BaseOrchestrator()
        mock_base = mock(ClaraBase("orchestrator_1",
                                   "localhost",
                                   int(xMsgConstants.DEFAULT_PORT),
                                   "localhost",
                                   int(xMsgConstants.DEFAULT_PORT)))

        self.orchestrator.base = mock_base

    def test_constructor_creates_object_and_sets_proper_name(self):
        self.assertIsInstance(self.orchestrator, BaseOrchestrator)

    def test_exit_dpe(self):
        self.orchestrator.exit_dpe("129.57.114.94_python")
        verify(self.orchestrator.base).send(any(xMsgMessage))

    def test_deploy_container_does_correctly_generic_send(self):
        self.orchestrator.deploy_container("129.57.114.94_python:thecontainer")
        verify(self.orchestrator.base).send(any(xMsgMessage))

    def test_exit_container_does_correctly_generic_send(self):
        self.orchestrator.exit_container("129.57.114.94_python:thecontainer")
        verify(self.orchestrator.base).send(any(xMsgMessage))

    def test_deploy_service_does_correctly_generic_send(self):
        self.orchestrator.deploy_service("129.57.114.94_python:thecontainer:S1",
                                         "clara.services.SERVICES")
        verify(self.orchestrator.base).send(any(xMsgMessage))

    def test_remove_service_does_correctly_generic_send(self):
        self.orchestrator.remove_service("129.57.114.94_python:thecontainer:S1")
        verify(self.orchestrator.base).send(any(xMsgMessage))

