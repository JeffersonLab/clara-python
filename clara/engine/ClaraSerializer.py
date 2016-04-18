# coding=utf-8

from abc import ABCMeta, abstractmethod


class ClaraSerializer:

    __metaclass__ = ABCMeta

    @abstractmethod
    def write(self, data):
        """Serializes the user object into a byte buffer and returns it
        It should return a byte buffer
        """
        pass

    @abstractmethod
    def read(self, byte_buffer):
        """De-Serializes the byte buffer into the user object and returns it
        """
        pass
