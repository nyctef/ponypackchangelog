import unittest
import sys
from impl import compare

class TestCompare(unittest.TestCase):

    def test_equality(self):
        result = compare.compare({"foo": "bar"}, {"foo": "bar"})
        self.assertEqual(result, {"foo": "<same>"})

    def test_equality2(self):
        result = compare.compare({"foo": "bar", "bar": "baz"}, {"foo": "bar", "bar": "baz"})
        self.assertEqual(result, {"foo": "<same>", "bar": "<same>"})

    def test_added(self):
        result = compare.compare({}, {"foo": "bar"})
        self.assertEqual(result, {"foo": "<added>"})

    def test_added2(self):
        result = compare.compare({"bar": "baz"}, {"foo": "bar", "bar": "baz"})
        self.assertEqual(result, {"bar": "<same>", "foo": "<added>"})

    def test_removed(self):
        result = compare.compare({"foo": "bar"}, {})
        self.assertEqual(result, {"foo": "<removed>"})

    def test_removed2(self):
        result = compare.compare({"foo": "bar", "bar": "baz"}, {"bar": "baz"})
        self.assertEqual(result, {"bar": "<same>", "foo": "<removed>"})

    def test_keychanged(self):
        result = compare.compare({"foo": "bar"}, {"baz": "bar"})
        self.assertEqual(result, {"baz": "<added>", "foo": "<removed>"})

    def test_valuechanged(self):
        result = compare.compare({"foo": "bar"}, {"foo": "asdf"})
        self.assertEqual(result, {"foo": ("bar", "asdf")})

    def test_valuechanged2(self):
        result = compare.compare({"foo": "bar", "bar": "baz"}, {"foo": "asdf", "bar": "baz"})
        self.assertEqual(result, {"bar": "<same>", "foo": ("bar", "asdf")})

if __name__ == '__main__':
    unittest.main()