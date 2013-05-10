#!/usr/bin/env python

"""
tests for mozfile.load
"""

import mozhttpd
import os
import tempfile
import unittest
from mozfile import load

class TestLoad(unittest.TestCase):
    """test the load function"""

    def test_http(self):
    """test with mozhttpd and a http:// URL"""
    httpd = mozhttpd.MozHttpd(port=8888,
                              urlhandlers=[{'method': 'GET',
                                            'path': '.*',
                                            '': lambda x: x}])
    httpd.start(block=False)


    def test_file_path(self):
        """test loading from file path"""
        try:
            # create a temporary file
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write('foo bar')
            tmp.close()

            # read the file
            contents = file(tmp.name).read()
            self.assertEqual(contents, 'foo bar')

            # read the file with load and a file path
            self.assertEqual(load(tmp.name).read(), contents)

            # read the file with load and a file URL
            self.assertEqual(load('file://%s' % tmp.name).read(), contents)
        finally:
            # remove the tempfile
            if os.path.exists(tmp.name):
                os.remove(tmp.name)

if __name__ == '__main__':
    unittest.main()
