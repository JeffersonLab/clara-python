# coding=utf-8

import unittest

from clara.base.ClaraAddress import ClaraAddress
from clara.base.ClaraNames import DpeName, ContainerName, ServiceName
from clara.base.ClaraLang import ClaraLang


class TestDpeName(unittest.TestCase):

    def test_dpe_name(self):
        dpe = DpeName("192.1.1.1", 7771, "python")
        self.assertIsInstance(dpe, DpeName)
        self.assertEqual(dpe.canonical_name(), "192.1.1.1_python")
        self.assertEqual(dpe.name(), dpe.canonical_name())
        self.assertEqual(str(ClaraLang.PYTHON), dpe.language())
        self.assertIsInstance(dpe.address(), ClaraAddress)


class TestContainerName(unittest.TestCase):

    def setUp(self):
        self.dpe = DpeName("192.1.1.1", 7771, "python")

    def test_container_name(self):
        container = ContainerName(self.dpe, "container1")
        self.assertIsInstance(container, ContainerName)

    def test_raises_exception(self):
        with self.assertRaises(TypeError):
            ContainerName("bla", "container2")


class TestServiceName(unittest.TestCase):

    def setUp(self):
        dpe = DpeName("192.1.1.1", 7771, "python")
        self.container = ContainerName(dpe, "container1")

    def test_container_name(self):
        service = ServiceName(self.container, "engine1")
        self.assertIsInstance(service, ServiceName)

    def test_raises_exception(self):
        with self.assertRaises(TypeError):
            ServiceName("container", "engine")

if __name__ == "__main__":
    unittest.main()
