#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import unittest

here = os.path.dirname(os.path.abspath(__file__))

class TestPlumbing(unittest.TestCase):
    """
    test piping mozprocess subprocesses
    """

    def command(self, command, *args):
        return [sys.executable, command] + list(args)

    def test_pipe(self):
        pass

if __name__ == '__main__':
    unittest.main()
