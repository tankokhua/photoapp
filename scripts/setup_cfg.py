#!/usr/bin/python
import os, sys, re
import glob

output = "bulkloader.yaml"
if len(sys.argv)==2:
   output = sys.argv[1]

cmd = "appcfg.py create_bulkloader_config --filename=%s --url=http://wizardry-tournament.appspot.com/_ah/remote_api" % output
print cmd
if os.path.exists(output):
   os.unlink(output)

os.system(cmd)
for tmpfile in glob.glob("bulkloader-*"):
    os.unlink(tmpfile)

results = []
for line in open(output):
    if re.search(r'connector: #', line):
       line = line.replace('connector: #', 'connector: csv #')
    results.append(line)

f = open(output, 'w')
f.write(''.join(results))
f.close()
