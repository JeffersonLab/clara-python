# coding=utf-8

import json
from xmsg.core.xMsgConstants import xMsgConstants

from clara.util.reports.BaseReport import BaseReport


class ServiceReport(BaseReport):

    _engine_name = xMsgConstants.UNDEFINED
    _class_name = xMsgConstants.UNDEFINED
    _failure_count = xMsgConstants.UNDEFINED
    _shm_reads = xMsgConstants.UNDEFINED
    _shm_writes = xMsgConstants.UNDEFINED
    _bytes_received = xMsgConstants.UNDEFINED
    _bytes_sent = xMsgConstants.UNDEFINED
    _execution_time = xMsgConstants.UNDEFINED
    _version = xMsgConstants.UNDEFINED

    def __init__(self, name):
        self.name = name

    @property
    def engine_name(self):
        return self._engine_name

    @engine_name.setter
    def engine_name(self, engine_name):
        self._engine_name = engine_name

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, class_name):
        self._class_name = class_name

    @property
    def failure_count(self):
        return self._failure_count

    @failure_count.setter
    def failure_count(self, failure_count):
        self._failure_count = failure_count

    @property
    def shm_reads(self):
        return self._shm_reads

    @shm_reads.setter
    def shm_reads(self, shm_reads):
        self._shm_reads = shm_reads

    @property
    def shm_writes(self):
        return self._shm_writes

    @shm_writes.setter
    def shm_writes(self, shm_writes):
        self._shm_writes = shm_writes

    @property
    def bytes_received(self):
        return self._bytes_received

    @bytes_received.setter
    def bytes_received(self, bytes_received):
        self._bytes_received = bytes_received

    @property
    def bytes_sent(self):
        return self._bytes_sent

    @bytes_sent.setter
    def bytes_sent(self, bytes_sent):
        self._bytes_sent = bytes_sent

    @property
    def execution_time(self):
        return self._execution_time

    @execution_time.setter
    def execution_time(self, execution_time):
        self._execution_time = execution_time

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, v):
        self._version = v

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True)
