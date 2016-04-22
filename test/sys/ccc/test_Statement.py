# coding=utf-8

import unittest
from clara.sys.ccc.Statement import Statement


class TestStatement(unittest.TestCase):

    def test_parse_linking(self):
        statement = Statement("S1+S2+S3", "S1")
        self.assertEqual(statement.get_input_links(), set([]))
        self.assertEqual(statement.get_output_links(), set(['S2']))

        statement = Statement("S1+S2+S3", "S2")
        self.assertEqual(statement.get_input_links(), set(['S1']))
        self.assertEqual(statement.get_output_links(), set(['S3']))

        statement = Statement("S1+S2+S3", "S3")
        self.assertEqual(statement.get_input_links(), set(['S2']))
        self.assertEqual(statement.get_output_links(), set([]))

        statement = Statement("S1+S2,S3", "S2")
        self.assertEqual(statement.get_input_links(), set(['S1']))
        self.assertEqual(statement.get_output_links(), set([]))

        statement = Statement("S1,S2+S3", "S3")
        self.assertEqual(statement.get_input_links(), set(['S1','S2']))
        self.assertEqual(statement.get_output_links(), set([]))

if __name__ == "__main__":
    unittest.main()
