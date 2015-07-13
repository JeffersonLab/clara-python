
__author__ = 'gurjyan'
from abc import ABCMeta, abstractmethod
from core.xMsgConstants import xMsgConstants


class ACEngine(object):
    """
    Clara service engine abstract class
    """
    __metaclass__ = ABCMeta

    exception_string = xMsgConstants.UNDEFINED
    exception_severity = xMsgConstants.UNDEFINED

    @abstractmethod
    def execute(self, x):
        pass

    @abstractmethod
    def execute_group(self, *argv):
        pass

    @abstractmethod
    def configure(self, x):
        pass

    @abstractmethod
    def get_states(self, x):
        pass

    @abstractmethod
    def get_current_state(self, x):
        pass

    @abstractmethod
    def get_accepted_data_type(self, x):
        pass

    @abstractmethod
    def get_returned_data_type(self, x):
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
    def dispose(self):
        pass

    def get_exception_string(self):
        return self.exception_string

    def get_exception_severity(self):
        return self.exception_severity

    def set_exception(self, exception_string, severity):
        self.exception_string = exception_string
        self.exception_severity = severity

    def reset(self):
        self.exception_string = xMsgConstants.UNDEFINED
        self.exception_severity = xMsgConstants.UNDEFINED
