#!/usr/bin/env python

import sys, smtplib

if len(sys.argv) < 4:
	print "Syntax: %s server fromaddr toaddr [toaddr...]" % sys.argv[0]
	sys.exit(255)

server = sys.argv[1]
fromaddr = sys.argv[2]
toaddr = sys.argv[3:]

message = """To: %s
From: %s
Subject: Test message from simple.py

Hello,

This is a test message sent to you from simple.py and smtplib.
""" % (', '.join(toaddr), fromaddr)

s = smtplib.SMTP(server)
s.sendmail(fromaddr, toaddr, message)

print "Message successfully sent to  %d recipient(s)" % len(toaddr)

