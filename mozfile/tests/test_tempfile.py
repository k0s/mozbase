#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
tests for mozfile.NamedTemporaryFile
"""

import mozfile
import unittest

class TestNamedTemporaryFile(unittest.TestCase):

    def test_iteration(self):
        """ensure the line iterator works"""


    def test_delete(self):
        """ensure ``delete=True/False`` works as expected"""

        # make a deleteable file; ensure it gets cleaned up
        path = None
        with mozfile.NamedTemporaryFile(delete=True) as tf:
            path = tf.name
        self.assertTrue(isinstance(path, basestring))

        

if __name__ == '__main__':
    unittest.main()
