#!/usr/bin/env python


import getpass, poplib, sys

(host, user) = sys.argv[1:]
passwd = getpass.getpass()

p = poplib.POP3(host)

try:
	print "Attempting APOP authentication..."
	p.apop(user, passwd)

except poplib.error_proto:
	print "Attempting standard authentication..."
	try:
		p.user(user)
		p.pass_(passwd)
	except poplib.error_proto, e:
		print "Login failed:", e
		sys.exit(1)
status = p.stat()
print "Mailbox has %d message for a total of %d bytes" % (status[0], status[1])
p.quit()
