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
import tempfile
import unittest
import zipfile

# directory of this file
here = os.path.dirname(os.path.abspath(__file__))

def clone_addon(name, output=None, compress=True):
    """
    Make a testing addon from the empty addon template

    - name: name of the addon (used in the `id` and `name` fields)
    - output: path of output file or directory
    - compress: whether to compress into an XPI or not
    """

    # source install.rdf file
    template = os.path.join(here, 'addons', 'empty', 'install.rdf')
    assert os.path.exists(template), "'%s' not found" % template
    template = file(template).read()

    # lines to replace in the install.rdf file
    replace = {'<em:id>test-empty@quality.mozilla.org</em:id>': '<em:id>%s@quality.mozilla.org</em:id>' % name,
               '<em:name>Test Extension (empty)</em:name>': '<em:name>%s</em:name>' % name
               }
    for item, replacement in replace.items():
        template = template.replace(item, replacement)

    def write_xpi(contents, path):
        """write the xpi file to `path`"""
        import pdb; pdb.set_trace()

    # write it!
    # note: this pattern could be abstracted
    if output:
        if os.path.exists(output):
            if os.path.isdir(output):
                if compressed:
                    path = os.path.join(output, 'name.xpi')
                else:
                    with file(os.path.join(output, 'install.rdf'), 'w') as f:
                        f.write(template)
                    return output
            else:
                if not compressed:
                    raise AssertionError("Specified directory format for addon but you gave a file path: '%s'" % output)
                path = output
            write_xpi(template, path)
            return path
        else:
            if compressed:
                dirname = os.path.dirname(output)
                if dirname and not os.path.isdir(dirname):
                    os.makedirs(dirname)
                write_xpi(output)
                return output
            else:
                os.makedirs(output)
                with file(os.path.join(output, 'install.rdf'), 'w') as f:
                    f.write(template)
                return output
    else:
        if compressed:
            pass
        else:
            tmppath = 

class TestAddonBackup(unittest.TestCase):

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
