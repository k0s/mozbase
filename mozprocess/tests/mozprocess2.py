#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

class WaitForTest(unittest.TestCase):
    """This tests specifically the case reported in bug 671316"""

    def __init__(self, *args, **kwargs):

        # Ideally, I'd use setUpClass but that only exists in 2.7.
        # So, we'll do this make step now.
        self.proclaunch = make_proclaunch(here)
        unittest.TestCase.__init__(self, *args, **kwargs)






if __name__ == '__main__':
    unittest.main()
