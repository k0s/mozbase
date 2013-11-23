#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import imp
import mozprocess
import os
import subprocess
import sys
import unittest

here = os.path.dirname(os.path.abspath(__file__))
count = imp.load_source('count', os.path.join(here, 'count.py'))
toupper = imp.load_source('toupper', os.path.join(here, 'toupper.py'))

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

    number = 11000  # number to count to for count.py

    def command(self, command, *args):
        return [sys.executable, os.path.join(here, command)] + list(args)

    def count_command(self):
        return self.command('count.py', str(self.number))

    def toupper_command(self):
        return self.command('toupper.py')

    def write(self, filename, lines):
        directory = os.environ['HOME']
        filename = os.path.join(directory, filename)
        with file(filename, 'w') as f:
            for index, line in enumerate(lines):
                f.write('%d - %s\n' % (index, line))

    def test_pipe(self):
        """
        test piping one subprocess to another; see
        https://bugzilla.mozilla.org/show_bug.cgi?id=924253
        """

        process = mozprocess.ProcessHandlerMixin(self.count_command())
        process.run()
        pipe = mozprocess.ProcessHandler(self.toupper_command(),
                                         stdin=process.proc.stdout,
                                         processOutputLine=[lambda x: None]
                                         )
        pipe.run()
        status = process.wait()

        results = [toupper.toupper(i) for i in count.count(self.number)]
        self.assertEqual(len(results), self.number)
        if len(results) != len(pipe.output):
            for i in range(len(results)):
                if i >= len(pipe.output) - 1:
                    line = '(NULL)'
                    break
                if results[i] != pipe.output[i]:
                    line = pipe.output[i]
                    break
            print "Difference at line %s:" % (i+1)
            print "Actual:\n%s" % line
            print "Should be:\n%s" % results[i]
            self.write('results.txt', results)
            self.write('actual.txt', pipe.output)
        self.assertEqual(len(results), len(pipe.output))
        self.assertEqual(results, pipe.output)

    def test_subprocess(self):
        """control test for subprocess"""

if __name__ == '__main__':
    unittest.main()
