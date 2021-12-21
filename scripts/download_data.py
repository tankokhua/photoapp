#!/usr/bin/python
####################################################################################
# This script downloads data from the application in csv format.
# The datafile is stored in 'datadir'
# The filename follows the following convention: Kind -> kinds.csv
# If no argument is supplied, it will download all kinds.
# Alternatively, you can specify the datastore Kind to be downloaded.
####################################################################################
import os
import sys
import glob

APP_ID = 'wizardry-tournament'
URL    = 'http://%s.appspot.com' % APP_ID
CFG    = '%s_bulkloader.yaml' % APP_ID

kinds = [ 
          'User',
          'Order',
          'Whatsapp',
	]

if len(sys.argv)==2:
   if sys.argv[1] in kinds:
      kinds = [ sys.argv[1] ]
   else:
     print 'Kind must be one of the following %s' % repr(kinds) 
     sys.exit(1)

print "Downloading data for %s." % repr(kinds)

kind_lkup = {}
for kind in kinds:
    kind_lkup.setdefault(kind, {}).setdefault('datafile', 'datadir/%ss.csv' % kind.lower())

successes = []
failures = []


if not os.path.exists('datadir'):
   os.mkdir('datadir')

for kind in kinds:
    print "*"*(10 +len(kind))
    print "* Kind: %s *" % kind
    print "*"*(10 +len(kind))
    datafile = kind_lkup[kind]['datafile']
    if os.path.exists(datafile):
       os.unlink(datafile)
    cmd = "appcfg.py download_data --config_file=%s --filename=%s --kind=%s --url=%s/_ah/remote_api --db_filename=skip" % (CFG, datafile, kind, URL)
    if os.system(cmd)>>8:
       failures.append(kind)
    else:
       successes.append(kind)

if len(failures):
   print "\nThe following datastore Kinds are not downloaded %s." % repr(failures)
else:
   files = glob.glob('bulkloader-*')
   for file in files:
       os.unlink(file)
   
if len(successes):
   print "\nThe following datastore Kinds are downloaded %s." % repr(successes)
