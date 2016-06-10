# coding=utf-8

from abc import ABCMeta, abstractmethod


class EngineCallback(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def callback(self, data):
        pass
