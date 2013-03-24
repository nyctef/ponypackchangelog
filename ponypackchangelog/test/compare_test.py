import unittest
import compare

class TestCompare(unittest.TestCase):

    def test_equality(self):
        result = compare.compare({"foo": "bar"}, {"foo": "bar"})
        self.assertEqual(result, {"foo": "<same>"})