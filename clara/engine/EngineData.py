#
# Copyright (C) 2015. Jefferson Lab, CLARA framework (JLAB). All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its
# documentation for educational, research, and not-for-profit purposes,
# without fee and without a signed licensing agreement.
#
# Author Ricardo  Oyarzun
# Department of Experimental Nuclear Physics, Jefferson Lab.
#
# IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
# THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
# JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
# HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
from xmsg.core.xMsgConstants import xMsgConstants


class EngineData:

    data = str(xMsgConstants.UNDEFINED)
    metadata = str(xMsgConstants.UNDEFINED)

    def __init__(self, data, metadata):
        self.data = data
        self.metadata = metadata

    def get_mimetype(self):
        return self.metadata.mimeType

    def set_data(self, metadata, data):
        self.metadata = metadata
        self.data = data

    def get_description(self):
        return self.metadata.description

    def set_description(self, description):
        self.metadata.description = description

    def get_status(self):
        return self.metadata.status

    def get_engine_state(self):
        return self.metadata.senderState

    def set_engine_state(self, state):
        self.metadata.senderState = state

    def get_engine_name(self):
        return self.metadata.sender

    def get_communication_id(self):
        return self.metadata.communicationId

    def set_communication_id(self, communication_id):
        self.metadata.communicationId = communication_id

    def get_composition(self):
        return self.metadata.composition

    def get_execution_time(self):
        return self.metadata.executionTime
