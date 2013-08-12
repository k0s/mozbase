#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import tempfile
import unittest

from manifestparser import convert
from manifestparser import ManifestParser

here = os.path.dirname(os.path.abspath(__file__))

class TestDirectoryConversion(unittest.TestCase):
    """test conversion of a directory tree to a manifest structure"""

    files = ('foo', 'bar', 'fleem')

    def create_stub(self):
        """stub out a directory with files in it"""

        directory = tempfile.mkdtemp()
        for i in self.files:
            file(os.path.join(directory, i), 'w').write(i)
        subdir = os.path.join(directory, 'subdir')
        os.mkdir(subdir)
        file(os.path.join(subdir, 'subfile'), 'w').write('baz')
        return directory

    def test_directory_to_manifest(self):
        """
        Test our ability to convert a static directory structure to a
        manifest.
        """

        # create a stub directory
        stub = self.create_stub()
        try:
            self.assertTrue(os.path.exists(stub) and os.path.isdir(stub))

            # Make a manifest for it:
            self.assertEqual(convert([stub]),
                         """[%(stub)s/bar]
[%(stub)s/fleem]
[%(stub)s/foo]
[%(stub)s/subdir/subfile]""" % dict(stub=stub))
        except:
            raise
        finally:
            shutil.rmtree(stub) # cleanup

    def test_convert_directory_manifests_in_place(self):
        """
        keep the manifests in place
        """

        stub = self.create_stub()
        try:
            convert([stub], write='manifest.ini')
            self.assertEqual(sorted(os.listdir(stub)),
                             ['bar', 'fleem', 'foo', 'manifest.ini', 'subdir'])
            parser = ManifestParser()
            parser.read(os.path.join(stub, 'manifest.ini'))
            self.assertEqual([i['name'] for i in parser.tests],
                             ['subfile', 'bar', 'fleem', 'foo'])
            parser = ManifestParser()
            parser.read(os.path.join(stub, 'subdir', 'manifest.ini'))
            self.assertEqual(len(parser.tests), 1)
            self.assertEqual(parser.tests[0]['name'], 'subfile')
        except:
            raise
        finally:
            shutil.rmtree(stub)

    def test_manifest_ignore(self):
        """test manifest `ignore` parameter for ignoring directories"""

        stub = self.create_stub()
        try:
            convert([stub], write='manifest.ini', ignore=('subdir',))
            parser = ManifestParser()
            parser.read(os.path.join(stub, 'manifest.ini'))
            self.assertEqual([i['name'] for i in parser.tests],
                             ['bar', 'fleem', 'foo'])
            parser = ManifestParser()
            self.assertFalse(os.path.exists(os.path.join(stub, 'subdir', 'manifest.ini')))
        except:
            raise
        finally:
            shutil.rmtree(stub)


if __name__ == '__main__':
    unittest.main()
