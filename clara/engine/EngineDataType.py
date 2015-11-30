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

from clara.engine.ClaraSerializer import ClaraSerializer


class Mimetype:

    SINT32 = u"binary/sint32"
    SINT64 = u"binary/sint64"
    SFIXED32 = u"binary/sfixed32"
    SFIXED64 = u"binary/sfixed64"
    FLOAT = u"binary/float"
    DOUBLE = u"binary/double"
    STRING = u"text/string"
    BYTES = u"binary/bytes"

    ARRAY_SINT32 = u"binary/array-sint32"
    ARRAY_SINT64 = u"binary/array-sint64"
    ARRAY_SFIXED32 = u"binary/array-sfixed32"
    ARRAY_SFIXED64 = u"binary/array-sfixed64"
    ARRAY_FLOAT = u"binary/array-float"
    ARRAY_DOUBLE = u"binary/array-double"
    ARRAY_STRING = u"text/array-string"
    ARRAY_BYTES = u"binary/array-string"

    NATIVE = u"native"


class EngineDataType:

    def __init__(self, mimetype, serializer):
        self.mimetype = mimetype
        self.serializer = serializer

    @classmethod
    def SINT32(cls):
        mimetype = Mimetype.SINT32
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def SINT64(cls):
        mimetype = Mimetype.SINT64
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def SFIXED32(cls):
        mimetype = Mimetype.SFIXED32
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def SFIXED64(cls):
        mimetype = Mimetype.SFIXED64
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def FLOAT(cls):
        mimetype = Mimetype.FLOAT
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def DOUBLE(cls):
        mimetype = Mimetype.DOUBLE
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def STRING(cls):
        mimetype = Mimetype.STRING
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_SINT32(cls):
        mimetype = Mimetype.ARRAY_SINT32
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_SINT64(cls):
        mimetype = Mimetype.ARRAY_SINT64
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_SFIXED32(cls):
        mimetype = Mimetype.ARRAY_SFIXED32
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_SFIXED64(cls):
        mimetype = Mimetype.ARRAY_SFIXED64
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_FLOAT(cls):
        mimetype = Mimetype.ARRAY_FLOAT
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_DOUBLE(cls):
        mimetype = Mimetype.ARRAY_DOUBLE
        return cls(mimetype, PrimitiveSerializer(mimetype))

    @classmethod
    def ARRAY_STRING(cls):
        mimetype = Mimetype.ARRAY_STRING
        return cls(mimetype, PrimitiveSerializer(mimetype))


class PrimitiveSerializer(ClaraSerializer):

    def __init__(self, mimetype):
        self.__mimetype = mimetype
        self.__native_serializer = NativeSerializer()

    def read(self, s_data):
        data = self.__native_serializer.read(s_data)

        if self.__mimetype == Mimetype.SINT32:
            return data.VLSINT32
        elif self.__mimetype == Mimetype.SINT64:
            return data.VLSINT64
        elif self.__mimetype == Mimetype.SFIXED32:
            return data.FLSINT32
        elif self.__mimetype == Mimetype.SFIXED64:
            return data.FLSINT64
        elif self.__mimetype == Mimetype.DOUBLE:
            return data.DOUBLE
        elif self.__mimetype == Mimetype.FLOAT:
            return data.FLOAT
        elif self.__mimetype == Mimetype.STRING:
            return data.STRING
        elif self.__mimetype == Mimetype.BYTES:
            return s_data.BYTES
        elif self.__mimetype == Mimetype.ARRAY_SINT32:
            return [d for d in data.VLSINT32A]
        elif self.__mimetype == Mimetype.ARRAY_SINT64:
            return [d for d in data.VLSINT64A]
        elif self.__mimetype == Mimetype.ARRAY_SFIXED32:
            return [d for d in data.FLSINT32A]
        elif self.__mimetype == Mimetype.ARRAY_SFIXED64:
            return [d for d in data.FLSINT64A]
        elif self.__mimetype == Mimetype.ARRAY_DOUBLE:
            return [d for d in data.DOUBLEA]
        elif self.__mimetype == Mimetype.ARRAY_FLOAT:
            return [d for d in data.FLOATA]
        elif self.__mimetype == Mimetype.ARRAY_STRING:
            return [d for d in data.STRINGA]

    def write(self, data):
        s_data = xMsgData()
        if self.__mimetype == Mimetype.SINT32:
            s_data.VLSINT32 = data
        elif self.__mimetype == Mimetype.SINT64:
            s_data.VLSINT64 = data
        elif self.__mimetype == Mimetype.SFIXED32:
            s_data.FLSINT32 = data
        elif self.__mimetype == Mimetype.SFIXED64:
            s_data.FLSINT64 = data
        elif self.__mimetype == Mimetype.DOUBLE:
            s_data.DOUBLE = data
        elif self.__mimetype == Mimetype.FLOAT:
            s_data.FLOAT = float(data)
        elif self.__mimetype == Mimetype.STRING:
            s_data.STRING = str(data)
        elif self.__mimetype == Mimetype.BYTES:
            s_data.BYTES = bytes(data)
        elif self.__mimetype == Mimetype.ARRAY_SINT32:
            s_data.VLSINT32A.extend(data)
        elif self.__mimetype == Mimetype.ARRAY_SINT64:
            s_data.VLSINT64A.extend(data)
        elif self.__mimetype == Mimetype.ARRAY_SFIXED32:
            s_data.FLSINT32A.extend(data)
        elif self.__mimetype == Mimetype.ARRAY_SFIXED64:
            s_data.FLSINT64A.extend(data)
        elif self.__mimetype == Mimetype.ARRAY_DOUBLE:
            s_data.DOUBLEA.extend(data)
        elif self.__mimetype == Mimetype.ARRAY_FLOAT:
            s_data.FLOATA.extend(data)
        elif self.__mimetype == Mimetype.ARRAY_STRING:
            s_data.STRINGA.extend(data)
        else:
            raise ValueError("Received invalid mimetype %s" % self.__mimetype)

        return self.__native_serializer.write(s_data)


class NativeSerializer(ClaraSerializer):

    def read(self, data):
        s_data = xMsgData()
        s_data.ParseFromString(data)
        return s_data

    def write(self, data):
        s_data = xMsgData()
        s_data.MergeFrom(data)
        return s_data.SerializeToString()


class RawSerializer(ClaraSerializer):

    def read(self, byte_buffer):
        return byte_buffer

    def write(self, data):
        return data
