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
		print "Client connection failed:", reasion
		reactor.stop()

class IMAPLogic:
	def __init__(self, proto):
		self.proto = proto
		self.factory = proto.factory
		d = self.proto.login(self.factory.username, self.factory.password)

		d.addCallback(lambda x: self.proto.examine('INBOX'))
		d.addCallback(self.examineresult)
		d.addCallback(self.logout)
		d.addCallback(self.stopreactor)

		d.addErrback(self.errorhappened)

	def examineresult(self, data):
		for key, value in data.items():
			if isinstance(value, tuple):
				print "%s: %s" % (key, ", ".join(value))
			else:
				print "%s: %s" % (key, value)

	def logout(self, data = None):
		return self.proto.logout()

	def stopreactor(self, failure):
		reactor.stop()

	def errorhappened(self, failure):
		print "An error occurred:", failure.getErrorMessage()
		d = self.logout()
		d.addBoth(self.stopreactor)
		return failure

password = getpass.getpass("Enter password for %s on %s: " % (sys.argv[2], sys.argv[1]))
reactor.connectTCP(sys.argv[1], 143, IMAPFactory(sys.argv[2], password))
reactor.run()
