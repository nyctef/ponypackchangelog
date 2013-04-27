import unittest
import sys
from impl import themefile

class TestParseLine(unittest.TestCase):

    def test_empty(self):
        self.assertEqual([], themefile._parse_line(""))

    def test_author(self):
        self.assertEqual([], themefile._parse_line("Author=ASDF"))

    def test_smile(self):
        self.assertEqual([(':)', 'smile.gif')], themefile._parse_line("smile.gif :)"))

    def test_smile2(self):
        self.assertEqual([(':)', 'smile.gif'), (':-)', 'smile.gif')], themefile._parse_line("smile.gif :) :-)"))

    def test_smile2_bang(self):
        self.assertEqual([(':)', 'smile.gif'), (':-)', 'smile.gif')], themefile._parse_line("! smile.gif :) :-)"))

class TestFromString(unittest.TestCase):

    def test_empty(self):
        self.assertEqual({}, themefile.from_string(""))

    def test_smile(self):
        self.assertEqual({':)': 'smile.gif'}, themefile.from_string("smile.gif :)"))

    def test_smile2(self):
        self.assertEqual({':)': 'smile.gif', ':-)': 'smile.gif'}, themefile.from_string("smile.gif :) :-)"))

    def test_smile3(self):
        self.assertEqual({':)': 'smile.gif', ':-)': 'smile.gif'}, themefile.from_string("smile.gif :) \n ! smile.gif :-)"))
        
    def test_smile4(self):
        self.assertEqual({':)': 'smile.gif', ':-)': 'smile.gif'}, themefile.from_string("smile.gif :) \r\n ! smile.gif :-)"))