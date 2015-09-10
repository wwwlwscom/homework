#!/usr/bin/env python


from twisted.internet import defer, reactor, protocol
from twisted.mail.imap4 import IMAP4Client

import sys, getpass

class IMAPClient(IMAP4Client):
	def connectionMade(self):
		IMAPLogic(self)

class IMAPFactory(protocol.ClientFactory):
	protocol = IMAPClient

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def clientConnectionFailed(self, connector, reason):
		print "Client connection failed:", reason
		reactor.stop()

class IMAPLogic:
	def __init__(self, proto):
		self.proto = proto
		self.factory = proto.factory

		d = self.proto.login(self.factory.username, self.factory.password)
		
		d.addCallback(lambda x: self.proto.list('', '*'))
		d.addcallback(self.listresult)
		d.addCallback(self.logout)
		d.addCallback(self.stopreactor)
		
		d.addErrback(self.errorhappened)
	
	def listresult(self, data):
		print "%-35s %-5s %-37s" % ('Mailbox Name', 'Delim', 'Mailbox Flags')
		print '-' * 35, '-' * 5, '-' * 37
		for box in data:
			flags, delim, name = box
			print "%-35s %-5s %-37s" % (name, delim, ', '.join(flags))


	def logout(self):
		print "Logging out."
		d = self.proto.logout()
		return d

	def stopreactor(self, data = None):
		print "Stopping reactor."
		reactor.stop()

	def errorhappened(self, failure):
		print "An error occurred:", failure.getErrorMessage()
		print "Because of the error, I am logging out and stopping reactor..."
		d = self.logout()
		d.addBoth(self.stopreactor)
		return failure

password = getpass.getpass("Enter password for %s on %s: " % (sys.argv[2], sys.argv[1]))

reactor.connectTCP(sys.argv[1], 143, IMAPFactory(sys.argv[2], password))
reactor.run()

