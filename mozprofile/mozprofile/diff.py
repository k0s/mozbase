#!/usr/bin/env python

"""
diff two profile summaries
"""

import difflib
import profile
import optparse
import os
import sys



def diff(profile1, profile2):

    profiles = (profile1, profile2)
    profile = {}
    parts = {}
    parts_dict = {}
    for index in (0, 1):
        profile[index] = mozprofile.Profile(profile[0])
        parts[index] = profile.print_profile(return_parts=True)
        parts_dict[index] = dict(parts[index])

    # keys the first profile is missing
    first_missing = [i for i in parts_dict[1]
                     if i not in parts_dict[0]]
    parts[0].extend([(i, '') for i in first_missing])

    # diffs
    for key, value in parts[0]:
        import pdb; pdb.set_trace()

def diff_profiles(args=sys.argv[1:]):

    usage = '%prog [options] profile1 profile2'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)
    if len(args) != 2:
        parser.error("Must give two profile paths")
    missing = [arg for arg in args if not os.path.exists(arg)]
    if missing:
        parser.error("Profile not found: %s" % (', '.join(missing)))

    diffs = diff(*args)

if __name__ == '__main__':
    diff_profiles()
