#!/usr/bin/python
#
# rewrote clamnag.pl in python
#
# partly as the way the DB version is reported completely changed, so clamnag.pl had to be re-written
# and I dont know perl.
#

import os, sys, DNS

# DNS where we get the current engine and database version:
currentclamdns = 'current.cvd.clamav.net'

# command to query ClamAV on what engine and database version is installed:
clamversioncommand = "clamdscan -V"

ERRORS = {
     'OK' : 0,
     'WARNING' : 1,
     'CRITICAL' : 2,
     'UNKNOWN' : 3,
     'DEPENDENT' : 4
     };

try:
   dnsstring = DNS.dnslookup(currentclamdns,"txt")
except Exception, e:
   print "ERROR looking up Clam current version record,",currentclamdns,e
   sys.exit(ERRORS["CRITICAL"])

try:
   shouldbeversions = dnsstring[0][0].split(":")
except:
   print "ERROR splitting TXT record returned from DNS",dnsstring
   sys.exit(ERRORS["CRITICAL"])
   

version = os.popen(clamversioncommand)
versionlines = version.readlines()
if version.close() != None:
   print "ERROR running ",clamversioncommand
   sys.exit(ERRORS["CRITICAL"])

try:
   for line in versionlines:
      splitline = line.split(" ")
      if splitline[0] == 'ClamAV':
         dailydbversion = splitline[1].split("/")[1].strip()
	 engineversion = splitline[1].split("/")[0].strip()

   print "engine version is",engineversion, " daily db version is ",dailydbversion, 

   # grab the first 2 version numbers from the version, minor versions change too much for us to care i.e.
   # for version X.Y.Z ... dont worry if Z is lagging

   shouldbemajorversion =  shouldbeversions[0].split(".")[:2]
   currentmajorversion  =  engineversion.split(".")[:2]

except:
   print "ERROR parsing command output"
   sys.exit(ERRORS["CRITICAL"])

if shouldbemajorversion == currentmajorversion and dailydbversion == shouldbeversions[2]:
   print " this is up to date"
   sys.exit(ERRORS['OK'])
else:
   if dailydbversion != shouldbeversions[2]:
      print " database is not up to date, should be ",shouldbeversions[2]," but is ",dailydbversion
   if shouldbemajorversion != currentmajorversion:
      print " clamav software not up to date, should be ",shouldbemajorversion," but is ",currentmajorversion
   sys.exit(ERRORS['WARNING'])
