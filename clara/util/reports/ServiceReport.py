# coding=utf-8

import json

from xmsg.core.xMsgConstants import xMsgConstants

from clara.util.reports.BaseReport import BaseReport


class ServiceReport(BaseReport):

    engine_name = xMsgConstants.UNDEFINED
    class_name = xMsgConstants.UNDEFINED
    version = xMsgConstants.UNDEFINED

    def __init__(self, service, engine):
        super(ServiceReport, self).__init__(service.myname,
                                            engine.get_author(),
                                            engine.get_description())
        self.engine_name = service.myname
        self.class_name = service.get_engine_name()
        self.version = engine.get_version()
        self.n_failures = self.n_requests = 0
        self.shm_reads = self.shm_writes = 0
        self.bytes_recv = self.bytes_sent = 0
        self.exec_time = 0

    def increment_failure_count(self):
        self.n_failures += 1

    def increment_shm_reads(self):
        self.shm_reads += 1

    def increment_shm_writes(self):
        self.shm_writes += 1

    def increment_bytes_received(self, bytes_received):
        self.bytes_recv += bytes_received

    def increment_bytes_sent(self, bytes_sent):
        self.bytes_sent += bytes_sent

    def increment_execution_time(self, execution_time):
        self.exec_time += execution_time

    def increment_request_count(self):
        self.n_requests += 1

    def to_json(self):
        return json.dumps(self.as_dict(), sort_keys=True)

    def to_str(self):
        return self.as_dict()
