#!/usr/bin/env python

import sys, smtplib, socket

fromaddr = 'wwwlwscom@163.com'
toaddr = sys.argv[1]

message = """To: %s
From: %s
Subject: Test message from simple.py

Hello,

This is a test message sent to you from simple.py and smtplib.
""" % (', '.join(toaddr), fromaddr)

try:
	s = smtplib.SMTP('smtp.163.com')
	code = s.ehlo()[0]
	usesesmtp = 1
	if not (200 <= code <= 299):
		usesesmtp = 0
		code = s.helo()[0]
		if not (200 <= code <= 299):
			raise SMTPHeloError(code, resp)
	if usesesmtp and s.has_extn('size'):
		print "Maximum message size is", s.esmtp_features['size']
		if len(message) > int(s.esmtp_features['size']):
			print "Message too large; aborting."
			sys.exit(2)
	s.login(fromaddr,'Sbyne9tg')
	s.set_debuglevel(1)
	s.sendmail(fromaddr, toaddr, message)
except (socket.gaierror,socket.error,socket.herror,smtplib.SMTPException), e:
	print " *** Your message may not have been sent!"
	print e
	sys.exit(1)
else:
	print "Message successfully sent to  %d recipient(s)" % len(toaddr)

