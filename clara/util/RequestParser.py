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
from xmsg.data.xMsgData_pb2 import xMsgData


class RequestParser(object):

    def __init__(self, data):
        """

        Args:
            data (String): data request string
        """
        self.cmd_data = data
        self.tokens = data.split("?")

    @classmethod
    def build_from_data(cls, data):
        """
        Args:
            data (xMsgData): proto buffer data object

        Returns:
            RequestParser object
        """
        if data.STRING:
            return cls(data.STRING)

        else:
            raise Exception("Empty data...")

    @classmethod
    def build_from_message(cls, msg):
        """
        Args:
            msg (xMsgMessage): proto buffer data object

        Returns:
            RequestParser object
        """
        mimetype = msg.get_metadata().dataType

        if mimetype == "binary/native":
            try:
                data = xMsgData.ParseFromString(msg.get_data)
                return cls(data)

            except Exception as e:
                print e
        else:
            raise Exception("Invalid mime-type = " + mimetype)

    def next_string(self):
        try:
            return self.tokens.pop()

        except IndexError:
            raise Exception("Invalid request: " + self.cmd_data)

    def next_integer(self):
        try:
            return int(self.tokens.pop())

        except IndexError:
            raise Exception("Invalid request: " + self.cmd_data)
