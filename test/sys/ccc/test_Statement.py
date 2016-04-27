# coding=utf-8

import unittest
from clara.sys.ccc.Statement import Statement


class TestStatement(unittest.TestCase):

    def test_service_name_in_the_beginning(self):
        statement = Statement("S1+S2+S3", "S1")
        self.assertEqual(statement.get_input_links(), set([]))
        self.assertEqual(statement.get_output_links(), set(['S2']))

    def test_service_name_in_the_middle(self):
        statement = Statement("S1+S2+S3", "S2")
        self.assertEqual(statement.get_input_links(), set(['S1']))
        self.assertEqual(statement.get_output_links(), set(['S3']))

    def test_service_name_at_the_end(self):
        statement = Statement("S1+S2+S3", "S3")
        self.assertEqual(statement.get_input_links(), set(['S2']))
        self.assertEqual(statement.get_output_links(), set([]))

    def test_branching_service_at_the_beginning(self):
        statement = Statement("S1+S2,S3", "S2")
        self.assertEqual(statement.get_input_links(), set(['S1']))
        self.assertEqual(statement.get_output_links(), set([]))

    def test_branching_service_at_the_end(self):
        statement = Statement("S1,S2+S3", "S3")
        self.assertEqual(statement.get_input_links(), set(['S1','S2']))
        self.assertEqual(statement.get_output_links(), set([]))

if __name__ == "__main__":
    unittest.main()
