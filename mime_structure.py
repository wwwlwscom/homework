#!/usr/bin/env python

import sys, email

def printmsg(msg, level = 0):
	l = "| " * level
	l2 = l + "|"
	print l + "+ Message Headers:"
	for header, value in msg.items():
		print l2, header + ":", value
	if msg.is_multipart():
		for item in msg.get_payload():
			print msg(item, level + 1)

msg = email.message_from_file(sys.stdin)
print (msg)

