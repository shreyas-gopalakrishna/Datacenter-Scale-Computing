#!/usr/bin/env python
"""mapper.py"""

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    # split the line into CSV fields
    words = line.split(",")

    if len(words) == 2:
        #
        # It's a citation
        #
        try:
            cite = long(words[0])
            print('%s\t%s' % (words[0], 'y'))
        except Exception as e:
            # improperly formed citation number
            print("Exception ", e);
            pass
    else:
        #
        # It's patent info 
        #
        try:
            cite = long(words[0])
            print('%s\t%s' % (words[0], ','.join(words[1:])))
        except Exception as e:
            # improperly formed citation number
            print("Exception ", e);
            pass

