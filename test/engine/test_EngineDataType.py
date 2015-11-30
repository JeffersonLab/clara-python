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
import unittest

from clara.engine.EngineDataType import Mimetype, EngineDataType, PrimitiveSerializer


class TestEngineDataType(unittest.TestCase):

    def test_mimetype_proper_returns(self):
        self.assertEqual(Mimetype.SINT32, u"binary/sint32")
        self.assertEqual(Mimetype.SINT64, u"binary/sint64")
        self.assertEqual(Mimetype.SFIXED32, u"binary/sfixed32")
        self.assertEqual(Mimetype.SFIXED64, u"binary/sfixed64")
        self.assertEqual(Mimetype.FLOAT, u"binary/float")
        self.assertEqual(Mimetype.DOUBLE, u"binary/double")
        self.assertEqual(Mimetype.STRING, u"text/string")
        self.assertEqual(Mimetype.BYTES, u"binary/bytes")

        self.assertEqual(Mimetype.ARRAY_SINT32, u"binary/array-sint32")
        self.assertEqual(Mimetype.ARRAY_SINT64, u"binary/array-sint64")
        self.assertEqual(Mimetype.ARRAY_SFIXED32, u"binary/array-sfixed32")
        self.assertEqual(Mimetype.ARRAY_SFIXED64, u"binary/array-sfixed64")
        self.assertEqual(Mimetype.ARRAY_FLOAT, u"binary/array-float")
        self.assertEqual(Mimetype.ARRAY_DOUBLE, u"binary/array-double")
        self.assertEqual(Mimetype.ARRAY_STRING, u"text/array-string")
        self.assertEqual(Mimetype.ARRAY_BYTES, u"binary/array-string")

    def test_proper_construction_of_types(self):
        SINT32 = EngineDataType.SINT32()
        self.assertEqual(SINT32.mimetype, Mimetype.SINT32)
        self.assertIsInstance(SINT32.serializer, PrimitiveSerializer)
        SINT64 = EngineDataType.SINT64()
        self.assertEqual(SINT64.mimetype, Mimetype.SINT64)
        self.assertIsInstance(SINT64.serializer, PrimitiveSerializer)
        SFIXED32 = EngineDataType.SFIXED32()
        self.assertEqual(SFIXED32.mimetype, Mimetype.SFIXED32)
        self.assertIsInstance(SFIXED32.serializer, PrimitiveSerializer)
        SFIXED64 = EngineDataType.SFIXED64()
        self.assertEqual(SFIXED64.mimetype, Mimetype.SFIXED64)
        self.assertIsInstance(SFIXED64.serializer, PrimitiveSerializer)
        FLOAT = EngineDataType.FLOAT()
        self.assertEqual(FLOAT.mimetype, Mimetype.FLOAT)
        self.assertIsInstance(FLOAT.serializer, PrimitiveSerializer)
        DOUBLE = EngineDataType.DOUBLE()
        self.assertEqual(DOUBLE.mimetype, Mimetype.DOUBLE)
        self.assertIsInstance(DOUBLE.serializer, PrimitiveSerializer)
        STRING = EngineDataType.STRING()
        self.assertEqual(STRING.mimetype, Mimetype.STRING)
        self.assertIsInstance(STRING.serializer, PrimitiveSerializer)
        ASINT32 = EngineDataType.ARRAY_SINT32()
        self.assertEqual(ASINT32.mimetype, Mimetype.ARRAY_SINT32)
        self.assertIsInstance(ASINT32.serializer, PrimitiveSerializer)
        ASINT64 = EngineDataType.ARRAY_SFIXED64()
        self.assertEqual(ASINT64.mimetype, Mimetype.ARRAY_SFIXED64)
        self.assertIsInstance(ASINT64.serializer, PrimitiveSerializer)
        ASFIXED32 = EngineDataType.ARRAY_SFIXED32()
        self.assertEqual(ASFIXED32.mimetype, Mimetype.ARRAY_SFIXED32)
        self.assertIsInstance(SFIXED32.serializer, PrimitiveSerializer)
        ASFIXED64 = EngineDataType.ARRAY_SFIXED64()
        self.assertEqual(ASFIXED64.mimetype, Mimetype.ARRAY_SFIXED64)
        self.assertIsInstance(ASFIXED64.serializer, PrimitiveSerializer)
        AFLOAT = EngineDataType.ARRAY_FLOAT()
        self.assertEqual(AFLOAT.mimetype, Mimetype.ARRAY_FLOAT)
        self.assertIsInstance(AFLOAT.serializer, PrimitiveSerializer)
        ADOUBLE = EngineDataType.ARRAY_DOUBLE()
        self.assertEqual(ADOUBLE.mimetype, Mimetype.ARRAY_DOUBLE)
        self.assertIsInstance(ADOUBLE.serializer, PrimitiveSerializer)
        ASTRING = EngineDataType.ARRAY_STRING()
        self.assertEqual(ASTRING.mimetype, Mimetype.ARRAY_STRING)
        self.assertIsInstance(ASTRING.serializer, PrimitiveSerializer)

    def test_serializers_set_and_get_methods(self):
        p_serializer = PrimitiveSerializer(Mimetype.SINT32)
        data = p_serializer.write(2)
        self.assertEqual(p_serializer.read(data), 2)
        p_serializer = PrimitiveSerializer(Mimetype.SINT64)
        data = p_serializer.write(200000000000000)
        self.assertEqual(p_serializer.read(data), 200000000000000)
        p_serializer = PrimitiveSerializer(Mimetype.SFIXED32)
        data = p_serializer.write(2)
        self.assertEqual(p_serializer.read(data), 2)
        p_serializer = PrimitiveSerializer(Mimetype.SFIXED64)
        data = p_serializer.write(200000000000000)
        self.assertEqual(p_serializer.read(data), 200000000000000)
        p_serializer = PrimitiveSerializer(Mimetype.DOUBLE)
        data = p_serializer.write(2.0)
        self.assertEqual(p_serializer.read(data), 2.0)
        p_serializer = PrimitiveSerializer(Mimetype.FLOAT)
        data = p_serializer.write(2.0)
        self.assertEqual(p_serializer.read(data), 2.0)
        p_serializer = PrimitiveSerializer(Mimetype.STRING)
        data = p_serializer.write("HELLO WORLD!")
        self.assertEqual(p_serializer.read(data), "HELLO WORLD!")
        p_serializer = PrimitiveSerializer(Mimetype.ARRAY_STRING)
        data = p_serializer.write(["HELLO", "WORLD!"])
        self.assertEqual(p_serializer.read(data), ["HELLO", "WORLD!"])
        p_serializer = PrimitiveSerializer(Mimetype.ARRAY_SINT32)
        data = p_serializer.write([1, 2, 3])
        self.assertEqual(p_serializer.read(data), [1, 2, 3])
        p_serializer = PrimitiveSerializer(Mimetype.ARRAY_SINT64)
        data = p_serializer.write([1, 2, 3])
        self.assertEqual(p_serializer.read(data), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
