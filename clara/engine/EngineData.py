# coding=utf-8


class EngineData(object):

    def __init__(self, data, metadata):
        self._data = data
        self._metadata = metadata

    def __repr__(self):
        return "EngineData: %s data" % self._metadata.dataType

    @property
    def mimetype(self):
        return self._metadata.mimeType

    def metadata(self):
        return self._metadata

    def get_data(self):
        return self._data

    def set_data(self, metadata, data):
        self._metadata = metadata
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

    def get_composition(self):
        return self._metadata.composition

    def get_execution_time(self):
        return self._metadata.executionTime
