# coding=utf-8

import json

from xmsg.core.xMsgConstants import xMsgConstants

from clara.util.reports.BaseReport import BaseReport


class ServiceReport(BaseReport):

    engine_name = xMsgConstants.UNDEFINED
    class_name = xMsgConstants.UNDEFINED
    failure_count = xMsgConstants.UNDEFINED
    shm_reads = xMsgConstants.UNDEFINED
    shm_writes = xMsgConstants.UNDEFINED
    bytes_received = xMsgConstants.UNDEFINED
    bytes_sent = xMsgConstants.UNDEFINED
    execution_time = xMsgConstants.UNDEFINED
    version = xMsgConstants.UNDEFINED

    def __init__(self, service, engine):
        super(ServiceReport, self).__init__(service.myname,
                                            engine.get_author(),
                                            engine.get_description())
        self.engine_name = engine.myname
        self.class_name = service.get_engine_name()
        self.version = engine.get_version

    @property
    def engine_name(self):
        return self.engine_name

    @engine_name.setter
    def engine_name(self, engine_name):
        self.engine_name = engine_name

    @property
    def class_name(self):
        return self.class_name

    @class_name.setter
    def class_name(self, class_name):
        self.class_name = class_name

    @property
    def failure_count(self):
        return self.failure_count

    @failure_count.setter
    def failure_count(self, failure_count):
        self.failure_count = failure_count

    @property
    def shm_reads(self):
        return self.shm_reads

    @shm_reads.setter
    def shm_reads(self, shm_reads):
        self.shm_reads = shm_reads

    @property
    def shm_writes(self):
        return self.shm_writes

    @shm_writes.setter
    def shm_writes(self, shm_writes):
        self.shm_writes = shm_writes

    @property
    def bytes_received(self):
        return self.bytes_received

    @bytes_received.setter
    def bytes_received(self, bytes_received):
        self.bytes_received = bytes_received

    @property
    def bytes_sent(self):
        return self.bytes_sent

    @bytes_sent.setter
    def bytes_sent(self, bytes_sent):
        self.bytes_sent = bytes_sent

    @property
    def execution_time(self):
        return self.execution_time

    @execution_time.setter
    def execution_time(self, execution_time):
        self.execution_time = execution_time

    @property
    def version(self):
        return self.version

    @version.setter
    def version(self, v):
        self.version = v

    def to_json(self):
        return json.dumps(self.__dict__, sort_keys=True)
