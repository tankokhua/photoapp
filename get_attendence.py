#!/usr/bin/python

import re, sys

cnt = 0
info = {}
for line in open('a.txt'):
    tokens = line.split('|')
    name = tokens[0]
    going = tokens[1]
    tstamp = tokens[-1]
    if going == 'yes':
       if tstamp in info:
          print "duplicate time stamp"
          sys.exit(1)
       info[tstamp]= name
       cnt+=1

n = 0
districts = {}
for a in sorted(info.keys()):
    name = info[a]
    if name in ['tankokhua','chankl','derzhan','dhika','ggerard','siangleong','chuakc','rogerhor','chuaszemin']:
       continue
    dno = n%8+1
    n+=1
    districts.setdefault(dno,[]).append(name)

f= open('usernames.txt','w')
for d in districts:
    print d, districts[d]
    for n in districts[d]:
        f.write("%s %d\n" % (n, d))
f.close()
