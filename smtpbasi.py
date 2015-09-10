#!/usr/bin/env python

import sys, smtplib, socket

fromaddr = 'wwwlwscom@163.com'
toaddr = 'wwwlwscom@hotmail.com'

message = """To: %s
From: %s
Subject: Test message from simple.py

Hello,

This is a test message sent to you from simple.py and smtplib.
""" % (', '.join(toaddr), fromaddr)
try:
	s = smtplib.SMTP('SMTP.163.com')
	s.set_debuglevel(1)
	s.docmd('ehlo','wwwlwscom@163.com')
	s.login(fromaddr,'Sbyne9tg')
	s.sendmail(fromaddr, toaddr, message)
except (socket.gaierror,socket.error,socket.herror,smtplib.SMTPException), e:
	print " *** Your message may not have been sent!"
	print e
	sys.exit(1)
else:
	print "Message successfully sent to  %d recipient(s)" % len(toaddr)

