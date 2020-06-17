#!/usr/bin/env python
"""reducer.py"""
from __future__ import print_function
from operator import itemgetter
import sys

current_patent = None
current_patent_info = None
current_patent_citations = []

def outputPatentInfo():
    global current_patent
    global current_patent_info
    global current_patent_citations

    if current_patent != None and current_patent_info != None:
        try:
            citations = int(current_patent_info[11])
            #print(len(current_patent_citations),"current_patent_citations")
            if citations == len(current_patent_citations):
                # print("%s\tok" % (current_patent))
                # counts match, so output all patent
                for patent in current_patent_citations:
                    print("%s\t%s" % (current_patent, current_patent_info[4]+","+ patent),end='')                
            else:
                # counts don't match. Ignore the patent.
                # print("%s\tbad %d vs %d " % (current_patent, citations, len(current_patent_citations)))
                pass
            print("%s\t%s" % (current_patent, ','.join(current_patent_info)),end='')
        except ValueError:
            #
            # Something wrong in number format
            #
            pass
        except Exception as e:
            print("Something died", e)

    current_patent = None
    current_patent_info = None
    current_patent_citations = []

def main():
    global current_patent
    global current_patent_info
    global current_patent_citations

    current_patent = None
    debug = False

    # input comes from STDIN
    for line in sys.stdin:
        # line.strip("\n")
        # parse the input we got from mapper.py

        key, value = line.split('\t', 1)

        # convert count (currently a string) to int
        try:
            patent = int(key)
        except ValueError:
            # key was not a number, so silently
            # ignore/discard this line
            continue

        # this IF-switch only works because Hadoop sorts map output
        # by key (here: word) before it is passed to the reducer

        if current_patent != patent:
            outputPatentInfo()

        current_patent = patent
        fields = value.split(',')

        if len(fields) > 1:
            current_patent_info = fields
        else:
            current_patent_citations.append(value)
        
    # do not forget to output the last word if needed!
    outputPatentInfo()


main()
