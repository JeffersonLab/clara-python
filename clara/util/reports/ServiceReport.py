# coding=utf-8

import json

from xmsg.core.xMsgConstants import xMsgConstants

from clara.util.reports.BaseReport import BaseReport


class ServiceReport(BaseReport):

    _engine_name = xMsgConstants.UNDEFINED
    _class_name = xMsgConstants.UNDEFINED
    _version = xMsgConstants.UNDEFINED

    _failure_count = 0
    _shm_reads = _shm_writes = 0
    _bytes_received = _bytes_sent = 0
    _execution_time = 0

    def __init__(self, service, engine):
        super(ServiceReport, self).__init__(service.myname,
                                            engine.get_author(),
                                            engine.get_description())
        self._engine_name = engine.myname
        self._class_name = service.get_engine_name()
        self._version = engine.get_version

    @property
    def failure_count(self):
        return self._failure_count

    def increment_failure_count(self):
        self._failure_count += 1

    @property
    def shm_reads(self):
        return self._shm_reads

    def increment_shm_reads(self):
        self._shm_reads += 1

    @property
    def shm_writes(self):
        return self._shm_writes

    def increment_shm_writes(self):
        self._shm_writes += 1

    @property
    def bytes_received(self):
        return self._bytes_received

    @bytes_received.setter
    def bytes_received(self, bytes_received):
        self._bytes_received += bytes_received

    @property
    def bytes_sent(self):
        return self._bytes_sent

    @bytes_sent.setter
    def bytes_sent(self, bytes_sent):
        self._bytes_sent += bytes_sent

    @property
    def execution_time(self):
        return self._execution_time

    @execution_time.setter
    def execution_time(self, execution_time):
        self._execution_time += execution_time

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True)
