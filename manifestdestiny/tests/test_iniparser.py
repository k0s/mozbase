#!/usr/bin/env python

"""
test .ini parsing

ensure our .ini parser is doing what we want; to be deprecated for
python's standard ConfigParser when 2.7 is reality so OrderedDict
is the default:

http://docs.python.org/2/library/configparser.html
"""

import unittest
from manifestparser import read_ini
from ConfigParser import ConfigParser
from StringIO import StringIO

class IniParserTest(unittest.TestCase):

    def test_inline_comments(self):
        """https://bugzilla.mozilla.org/show_bug.cgi?id=855288"""

        # test '#' inline comments
        string = """[test_felinicity.py]
kittens = true # This test requires kittens
"""
        buffer = StringIO()
        buffer.write(string)
        buffer.seek(0)
        result = read_ini(buffer)[0][1]['kittens']
        buffer.seek(0)
        parser = ConfigParser()
        parser.readfp(buffer)
        control = parser.get('test_felinicity.py', 'kittens')
        self.assertEqual(result, control)

        # test ';' inline comments
        string = string.replace('#', ';')
        buffer = StringIO()
        buffer.write(string)
        buffer.seek(0)
        result = read_ini(buffer)[0][1]['kittens']
        buffer.seek(0)
        parser = ConfigParser()
        parser.readfp(buffer)
        control = parser.get('test_felinicity.py', 'kittens')
        print ((result, control))
        self.assertEqual(result, control)


if __name__ == '__main__':
    unittest.main()
