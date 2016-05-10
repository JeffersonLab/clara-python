# coding=utf-8

from clara.sys.ccc.ServiceState import ServiceState


class ServiceSysConfig(object):

    def __init__(self, name, initial_state):
        self._state = ServiceState(name, initial_state)
        self._is_data_request = False
        self._is_done_request = False
        self._data_request_count = 0
        self._done_request_count = 0
        self._data_report_threshold = -1
        self._done_report_threshold = -1

    def add_request(self):
        self._data_request_count += 1
        self._done_request_count += 1

    def reset_data_request_count(self):
        self._data_request_count = 0

    def reset_done_request_count(self):
        self._done_request_count = 0

    @property
    def data_request(self):
        return self._is_data_request and\
               self._data_request_count >= self._data_report_threshold

    @data_request.setter
    def data_request(self, bool_flag):
        self._is_data_request = bool_flag

    def data_request_count(self):
        return self._data_request_count

    @property
    def done_request(self):
        return self._is_done_request and\
               self._done_request_count >= self._done_report_threshold

    @done_request.setter
    def done_request(self, bool_flag):
        self._is_done_request = bool_flag

    def done_request_count(self):
        return self._done_request_count

    @property
    def data_report_threshold(self):
        return self._data_report_threshold

    @data_report_threshold.setter
    def data_report_threshold(self, threshold):
        self._data_report_threshold = threshold

    @property
    def done_report_threshold(self):
        return self._done_report_threshold

    @done_report_threshold.setter
    def done_report_threshold(self, threshold):
        self._done_report_threshold = threshold

    def update_state(self, new_state):
        self._state.state = new_state
