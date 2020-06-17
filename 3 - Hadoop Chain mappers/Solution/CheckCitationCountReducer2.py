#!/usr/bin/env python
"""reducer2.py"""

from operator import itemgetter
import sys

current_patent = None
current_patent_info = None
current_patent_citations = []

for line in sys.stdin:
    if(line == "" or len(line) < 5):
        pass
    else:
        key = line.split('\t')[0].replace('\n','')
        values = line.split('\t')[1].replace('\n','')
        
        # convert count (currently a string) to int
        try:
            patent = int(key)
        except ValueError:
            continue
        if current_patent != patent:
            if current_patent != None and current_patent_info != None:                
                try:
                    for p in current_patent_citations:
                        print("%s\t%s" % (current_patent, current_patent_info[4]+","+ p))
                    print("%s\t%s" % (current_patent, ','.join(current_patent_info).replace('\r','')))
                except ValueError:
                    pass
                except Exception as e:
                    print("Something died", e)

            current_patent = None
            current_patent_info = None
            current_patent_citations = []
        
        current_patent = patent
        fields = values.split(',')
        
        if len(fields) > 2:
            current_patent_info = fields
        else:
            current_patent_citations.append(values)

if current_patent != None and current_patent_info != None:                
    try:
        for p in current_patent_citations:
            print("%s\t%s" % (current_patent, current_patent_info[4]+","+ p))
        print("%s\t%s" % (current_patent, ','.join(current_patent_info).replace('\r','')))
    except ValueError:
        pass
    except Exception as e:
        print("Something died", e)