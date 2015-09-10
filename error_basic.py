#!/usr/bin/env python


import sys, urllib2


req = urllib2.Request(req)

try:
	fd = urllib2.urlopen(req)
except urllib2.URLError, e:
	print "Error retrieving data:", e
	sys.exit(1)

print "Retrieved", fd.geturl()

info = fd.info()
for key, value in info.items():
	print "%s = %s" % (key, value)
