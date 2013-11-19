#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import subprocess
import traceback

from mozprocess.processhandler import ProcessHandler
import mozcrash
import mozlog

def abstractmethod(method):
  """decorator to mark a method as abstract"""
  line = method.func_code.co_firstlineno
  filename = method.func_code.co_filename
  def not_implemented(*args, **kwargs):
    raise NotImplementedError('Abstract method %s at File "%s", line %s '
                              'should be implemented by a concrete class' %
                              (repr(method), filename, line))
  return not_implemented

class RunnerNotStartedError(Exception):
    """Exception handler in case the runner is not started."""

class Runner(object):

    def __init__(self, profile, clean_profile=True, process_class=None,
                 kp_kwargs=None, env=None, symbols_path=None):
        self.clean_profile = clean_profile
        self.env = env or {}
        self.kp_kwargs = kp_kwargs or {}
        self.process_class = process_class or ProcessHandler
        self.process_handler = None
        self.returncode = None
        self.profile = profile
        self.log = mozlog.getLogger('MozRunner')
        self.symbols_path = symbols_path

    @abstractmethod
    def start(self, *args, **kwargs):
        """Run the process"""

    def wait(self, timeout=None):
        """
        Wait for the process to exit.
        Returns the process return code if the process exited,
        returns None otherwise.

        If timeout is not None, will return after timeout seconds.
        Use is_running() to determine whether or not a timeout occured.
        Timeout is ignored if interactive was set to True.
        """
        if self.process_handler is not None:
            if isinstance(self.process_handler, subprocess.Popen):
                self.returncode = self.process_handler.wait()
            else:
                self.process_handler.wait(timeout)
                self.returncode = self.process_handler.proc.poll()
                if self.returncode is not None:
                    self.process_handler = None
        elif self.returncode is None:
            raise RunnerNotStartedError("Wait called before runner started")

        return self.returncode

    def is_running(self):
        """
        Returns True if the process is still running, False otherwise
        """
        return self.process_handler is not None


    def stop(self):
        """
        Kill the process
        """
        if self.process_handler is None:
            return
        self.process_handler.kill()
        self.process_handler = None

    def reset(self):
        """
        Reset the runner to its default state
        """
        if getattr(self, 'profile', False):
            self.profile.reset()

    def check_for_crashes(self, dump_directory, test_name=None):
        crashed = False
        try:
            crashed = mozcrash.check_for_crashes(dump_directory,
                                                 self.symbols_path,
                                                 test_name=test_name)
        except:
            traceback.print_exc()
        return crashed

    def cleanup(self):
        """
        Cleanup all runner state
        """
        if self.is_running():
            self.stop()
        if getattr(self, 'profile', False) and self.clean_profile:
            self.profile.cleanup()

    __del__ = cleanup
