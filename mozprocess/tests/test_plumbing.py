#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozprocess
import os
import sys
import unittest

here = os.path.dirname(os.path.abspath(__file__))

class OutputHandler(object):
    """
    handler to store lines of output
    """
    def __init__(self):
        self.lines = []
    def __call__(self, line):
        self.lines.append(line)

class TestPlumbing(unittest.TestCase):
    """
    test piping mozprocess subprocesses
    """

    def command(self, command, *args):
        return [sys.executable, os.path.join(here, command)] + list(args)

    def test_pipe(self):
        """
        test piping one subprocess to another; see
        https://bugzilla.mozilla.org/show_bug.cgi?id=924253
        """

        process = mozprocess.ProcessHandlerMixin(self.command('count.py', '11'))
        process.run()
        pipe = mozprocess.ProcessHandler(self.command('toupper.py'), stdin=process.proc.stdout)
        pipe.run()
        status = process.wait()

if __name__ == '__main__':
    unittest.main()
