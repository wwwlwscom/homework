#!/usr/bin/env python

import sys, smtplib, socket

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

try:
	s = smtplib.SMTP(server)
	s.docmd('ehlo','wwwlwscom@163.com')
	s.login('wwwlwscom@163.com','Sbyne9tg')
	s.set_debuglevel(1)
	s.sendmail(fromaddr, toaddr, message)
except (socket.gaierror,socket.error,socket.herror,smtplib.SMTPException), e:
	print " *** Your message may not have been sent!"
	print e
	sys.exit(1)
else:
	print "Message successfully sent to  %d recipient(s)" % len(toaddr)

