#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import optparse
import os
import sys

mapping = {'0': 'zero',
           '1': 'one',
           '2': 'two',
           '3': 'three',
           '4': 'four',
           '5': 'five',
           '6': 'six',
           '7': 'seven',
           '8': 'eight',
           '9': 'nine'}

def int2str(integer):
    digits = []
    if integer < 0:
        digits.append('negative')
        integer = -integer
    digits.extend([mapping[digit] for digit in str(integer)])
    return ' '.join(digits)

def main(args=sys.argv[1:]):

    usage = '%prog [options] int <int> <...>'
    parser = optparse.OptionParser(usage=usage, description=__doc__)
    options, args = parser.parse_args(args)
    if not args:
        parser.error("No integer given")
    for arg in args:
        try:
            integer = int(arg)
        except ValueError:
            raise # TODO
        if integer > 0:
            for i in range(1, integer+1):
                print int2str(i)
        elif integer < 0:
            for i in range(-1, integer-1, -1):
                print int2str(i)
        else: # 0
            print int2str(i)

if __name__ == '__main__':
    main()
