#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozfile
import mozprofile
import os
import tempfile
import unittest

here = os.path.dirname(os.path.abspath(__file__))

class TestProfilePrint(unittest.TestCase):

    def test_profileprint(self):
        """
        test the print_profile function
        """

        keys = set(['Files', 'Path', 'Preferences, user.js'])
        ff_prefs = mozprofile.FirefoxProfile.preferences # shorthand
        pref_string = '\n'.join(['%s: %s' % (key, ff_prefs[key])
                                 for key in sorted(ff_prefs.keys())])

        tempdir = tempfile.mkdtemp()
        try:
            profile = mozprofile.FirefoxProfile(tempdir)
            parts = profile.print_profile(return_parts=True)
            parts = dict(parts)

            self.assertEqual(parts['Path'], tempdir)
            self.assertEqual(set(parts.keys()), keys)
            self.assertEqual(pref_string, parts['Preferences, user.js'].strip())

        except:
            raise
        finally:
            mozfile.rmtree(tempdir)

    def test_strcast(self):
        """
        test casting to a string
        """

        profile = mozprofile.Profile()
        self.assertEqual(str(profile), profile.print_profile())

    def test_profile_diff(self):
        profile1 = mozprofile.Profile()
        profile2 = mozprofile.Profile(preferences=dict(foo='bar'))

        # diff a profile against itself; no difference

if __name__ == '__main__':
    unittest.main()
