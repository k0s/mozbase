:mod:`mozprocess` --- Mozilla-authored process handling
=======================================================

mozprocess provides python process management via an operating system
and platform transparent interface to Mozilla platforms of interest.
Mozprocess aims to provide the ability
to robustly terminate a process (by timeout or otherwise), along with
any child processes, on Windows, OS X, and Linux. Mozprocess utilizes
and extends ``subprocess.Popen`` to these ends.


API
---

`mozprocess.processhandler:ProcessHandler <https://github.com/mozilla/mozbase/blob/master/mozprocess/mozprocess/processhandler.py>`_
is the central exposed API for mozprocess.  ``ProcessHandler`` utilizes
a contained subclass of `subprocess.Popen <http://docs.python.org/library/subprocess.html>`_ ,
``Process``, which does the brunt of the process management.

Basic usage::

    process = ProcessHandler(['command', '-line', 'arguments'],
                             cwd=None, # working directory for cmd; defaults to None
                             env={},   # environment to use for the process; defaults to os.environ
                             )
    process.run(timeout=60) # seconds
    process.wait()

``ProcessHandler`` extends ``ProcessHandlerMixin`` which by default prints the
output, logs to a file (if specified), and stores the output (if specified, by
default ``True``).  ``ProcessHandlerMixin``, by default, does none of these things
and has no handlers for ``onTimeout``, ``processOutput``, or ``onFinish``.

``ProcessHandler`` may be subclassed to handle process timeouts (by overriding
the ``onTimeout()`` method), process completion (by overriding
``onFinish()``), and to process the command output (by overriding
``processOutputLine()``).


Examples
--------

In the most common case, a process handler is created, then run followed by wait are called::

    proc_handler = ProcessHandler([cmd, args])
    proc_handler.run(outputTimeout=60) # will time out after 60 seconds without output
    proc_handler.wait()

Often, the main thread will do other things::

    proc_handler = ProcessHandler([cmd, args])
    proc_handler.run(timeout=60) # will time out after 60 seconds regardless of output
    do_other_work()

    if proc_handler.proc.poll() is None:
        proc_handler.wait()

By default output is printed to stdout, but anything is possible::

    # this example writes output to both stderr and a file called 'output.log'
    def some_func(line):
        print >> sys.stderr, line

        with open('output.log', 'a') as log:
            log.write('%s\n' % line)

    proc_handler = ProcessHandler([cmd, args], processOutputLine=some_func)
    proc_handler.run()
    proc_handler.wait()


TODO
----

* Document improvements over ``subprocess.Popen.kill``
* Introduce test the show improvements over ``subprocess.Popen.kill``

.. automodule:: mozprocess
   :members:
