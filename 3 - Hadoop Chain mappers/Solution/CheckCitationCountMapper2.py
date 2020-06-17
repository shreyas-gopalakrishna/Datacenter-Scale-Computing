#!/usr/bin/env python
"""mapper2.py"""

import sys

# input comes from STDIN (standard input)
for line in sys.stdin:
    if(line == "" or len(line) < 5):
        pass
    else:
        line.replace('\n','')
        key = line.split("\t")[0]
        values = line.split("\t")[1].split(',')
        if(len(values) < 3):
            try:
                print('%s\t%s' % (values[1].replace('\n',''), key+','+values[0]))
            except Exception as e:
                # improperly formed citation number
                print("Exception ", e)
        else:
            try:
                print('%s\t%s' % (key, ','.join(values).replace('\n','')))
            except Exception as e:
                # improperly formed citation number
                print("Exception ", e)
