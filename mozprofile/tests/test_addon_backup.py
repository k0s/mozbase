#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

"""
test addon backups;
see https://bugzilla.mozilla.org/show_bug.cgi?id=759594
and https://bugzilla.mozilla.org/show_bug.cgi?id=841086
"""

import os
import unittest

# directory of this file
here = os.path.dirname(os.path.abspath(__file__))


class TestAddonBackup(unittest.TestCase):

    def clone_addon(self, name, compress=True):
        """
        - name: name of the addon (e.g. 'empty' for the two in there)
        - compress: whether to compress into an XPI or not
        """

    def test_addon_backup(self):
        """
        prior to the resolution of bug 759594 if an adoon was installed to a
        profile that already had an addon in it, the original addon would be
        overwritten.  However, on cleanup, all addons were deleted
        See https://github.com/mozilla/mozbase/blob/bf6e6d20c6d6a47bbaa78103fcfeaee04cf76085/mozprofile/mozprofile/addons.py
        for the state of the code prior to the resolution of u 759594
        """


if __name__ == '__main__':
    unittest.main()
