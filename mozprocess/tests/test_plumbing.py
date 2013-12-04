#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import imp
import mozprocess
import os
import subprocess
import sys
import tempfile
import unittest
from StringIO import StringIO
TemporaryFile = tempfile.SpooledTemporaryFile

here = os.path.dirname(os.path.abspath(__file__))
count = imp.load_source('count', os.path.join(here, 'count.py'))
toupper = imp.load_source('toupper', os.path.join(here, 'toupper.py'))

class readmethod(object):
    """decorator for read methods"""
    def __init__(self, method):
        self.method = method
    def __call__(self, *args, **kwargs):
        print "Hi! %s" % self.method
        return self.method(*args, **kwargs)

class Buffer(TemporaryFile):

    def __call__(self, line):
        pos = self.tell()
        self.write(line + '\n')
        self.flush()
        #                print pos
        #self.seek(pos)

    @readmethod
    def read(self, *args):
        return TemporaryFile.read(self, *args)

    @readmethod
    def readline(self, *args):
        return TemporaryFile.readline(self, *args)

    @readmethod
    def readlines(self, *args):
        return TemporaryFile.readlines(self, *args)


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

    def count_command(self, number=None):
        if number is None:
            number = self.number
        return self.command('count.py', str(number))

    def toupper_command(self):
        return self.command('toupper.py')

    def results(self):
        """correct results"""
        return [toupper.toupper(i) for i in count.count(self.number)]

    def write(self, filename, lines):
        directory = os.environ['HOME']
        filename = os.path.join(directory, filename)
        with file(filename, 'w') as f:
            for index, line in enumerate(lines):
                f.write('%d - %s\n' % (index, line))

    def compare_lists(self, expected, output):
        """
        compare two lists
        """
        if (len(expected) != len(output)) or (expected != output):
            for i in range(len(expected)):
                if i >= len(output) - 1:
                    line = '(NULL)'
                    break
                if expected[i] != output[i]:
                    line = output[i]
                    break
            print "Difference at line %s:" % (i+1)
            print "Actual:\n%s" % line
            print "Should be:\n%s" % expected[i]
        self.assertEqual(len(expected), len(output))
        self.assertEqual(expected, output)

    def test_output(self):
        """
        test stdout processing
        """
        number = 1000000
        process = mozprocess.ProcessHandler(self.count_command(number),
                                            processOutputLine=[lambda x: None])
        process.run()
        status = process.wait()
        output = process.output
        self.assertEqual(status, 0)
        results = list(count.count(number))
        self.compare_lists(results, output)

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
        self.assertEqual(status, 0)

        results = self.results()
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

    def test_shell_pipe(self):
        """test using shell pipe -- `|` -- on systems which support it"""

        command = ' | '.join([subprocess.list2cmdline(command)
                              for command in (self.count_command(),
                                              self.toupper_command())
                              ])
        # subprocess
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   shell=True)
        output = process.communicate()[0]
        lines = output.splitlines()
        self.assertEqual(len(lines), self.number)

    def test_subprocess(self):
        """
        control test for subprocess; see
        http://docs.python.org/2/library/subprocess.html#replacing-shell-pipeline
        """

        p1 = subprocess.Popen(self.count_command(), stdout=subprocess.PIPE)
        p2 = subprocess.Popen(self.toupper_command(),
                              stdin=p1.stdout,
                              stdout=subprocess.PIPE)
        p1.stdout.close()
        output = p2.communicate()[0]
        lines = output.splitlines()
        self.assertEqual(len(lines), self.number)

    def test_subprocess_buffer(self):
        """
        illustrate use of subprocess.Popen with a file-like buffer
        """
        _buffer = Buffer()
        p1 = subprocess.Popen(self.count_command(), stdout=_buffer)
        p2 = subprocess.Popen(self.toupper_command(),
                              stdin=_buffer,
                              stdout=subprocess.PIPE)
        output = p2.communicate()[0]
        # ^ this doesn't work! :(

    def test_subprocess_pipe(self):
        _buffer = Buffer()
        p1 = subprocess.Popen(self.count_command(), stdout=_buffer)
        p2 = subprocess.Popen(self.toupper_command(),
                              stdin=_buffer,
                              stdout=subprocess.PIPE)
        output = p2.communicate()[0]

    def test_processOutputLine(self):
        """
        add a processOutputLine form of pipe
        """




        _buffer = Buffer()
        process = mozprocess.ProcessHandlerMixin(self.count_command(),
                                                 processOutputLine=[_buffer],
                                                 )
        process.run()
        pipe = mozprocess.ProcessHandler(self.toupper_command(),
                                         stdin=_buffer,
                                         processOutputLine=[lambda x: None]
                                         )
        pipe.run()
        status = process.wait()
        self.assertEqual(status, 0)
        output = pipe.output
        # XXX does not work properly :(
        #        self.assertEqual(len(output), self.number)
        #        self.assertEqual(output, self.results())

if __name__ == '__main__':
    unittest.main()
