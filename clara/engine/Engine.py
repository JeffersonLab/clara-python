# coding=utf-8

from abc import ABCMeta, abstractmethod


class Engine:

    __metaclass__ = ABCMeta

    @abstractmethod
    def configure(self, engine_data):
        pass

    @abstractmethod
    def execute(self, engine_data):
        pass

    @abstractmethod
    def execute_group(self, inputs):
        pass

    @abstractmethod
    def get_input_data_types(self):
        pass

    @abstractmethod
    def get_output_data_types(self):
        pass

    @abstractmethod
    def get_states(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_version(self):
        pass

    @abstractmethod
    def get_author(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def destroy(self):
        pass
