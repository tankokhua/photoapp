#!/usr/bin/python

import csv
import sys

results = []
with open('oct.csv', 'r') as csvfile:
     reader = csv.reader(csvfile)
     cnt = 0
     for row in reader:
	 if cnt == 0:
            header = row
	    fields = {}
	    for idx, f in enumerate(row):
         	fields.setdefault(f, idx)
	 else:
            results.append(row)
            print row[0].replace('@micron.com',''), row[1]
	 cnt+=1
sys.exit(0)
for x in results:
    print x[fields["lastname"]].split(",")[1]
     
