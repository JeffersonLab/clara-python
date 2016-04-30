# coding=utf-8

from xmsg.data.xMsgMeta_pb2 import xMsgMeta


class EngineData(object):
    _data = "Undefined"

    def __init__(self):
        super(EngineData, self).__init__()
        self._metadata = xMsgMeta()

    def __repr__(self):
        return "EngineData: %s data" % self._metadata.dataType

    @property
    def mimetype(self):
        return self._metadata.dataType

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata

    def get_data(self):
        return self._data

    def set_data(self, mimetype, data):
        self._metadata.dataType = mimetype
        self._data = data

    @property
    def description(self):
        return self._metadata.description

    @description.setter
    def description(self, description):
        self._metadata.description = description

    @property
    def status(self):
        return self._metadata.status

    @status.setter
    def status(self, status):
        self._metadata.senderState = status

    @property
    def state(self):
        return self._metadata.senderState

    @state.setter
    def state(self, state):
        self._metadata.senderState = state

    def engine_name(self):
        return self._metadata.author

    @property
    def communication_id(self):
        return self._metadata.communicationId

    @communication_id.setter
    def communication_id(self, communication_id):
        self._metadata.communicationId = communication_id

    @property
    def severity(self):
        return self._metadata.severityId

    @severity.setter
    def severity(self, severity):
        self._metadata.severityId = severity

    @property
    def composition(self):
        return self._metadata.composition

    @composition.setter
    def composition(self, composition):
        self._metadata.composition = composition

    def get_execution_time(self):
        return self._metadata.executionTime
