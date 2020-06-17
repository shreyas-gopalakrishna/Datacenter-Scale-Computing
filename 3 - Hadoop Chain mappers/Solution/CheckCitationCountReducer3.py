#!/usr/bin/env python
"""reducer3.py"""

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
        
        try:
            patent = int(key)
        except ValueError:
            continue
        if current_patent != patent:
            if current_patent != None and current_patent_info != None:                
                try:
                    count = 0
                    for p in current_patent_citations:
                        if(current_patent_info[4].replace('\r','').replace('\n','') == p.split(',')[2].replace('\r','').replace('\n','')):
                            count += 1
                    print("%s\t%s" % (current_patent, ','.join(current_patent_info).replace('\r','').replace('\n','')+','+str(count)))
                except ValueError:
                    pass
                except Exception as e:
                    print("Something died", e)

            current_patent = None
            current_patent_info = None
            current_patent_citations = []
        
        current_patent = patent
        fields = values.split(',')
        
        if len(fields) > 3:
            current_patent_info = fields
        else:
            current_patent_citations.append(values)

if current_patent != None and current_patent_info != None:                
    try:
        count = 0
        for p in current_patent_citations:
            if(current_patent_info[4].replace('\r','').replace('\n','') == p.split(',')[2].replace('\r','').replace('\n','')):
                count += 1
        print("%s\t%s" % (current_patent, ','.join(current_patent_info).replace('\r','').replace('\n','')+','+str(count)))
    except ValueError:
        pass
    except Exception as e:
        print("Something died", e)