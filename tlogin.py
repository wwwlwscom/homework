#!/usr/bin/env python


from twisted.internet import defer, reactor, protocol
from twisted.mail.imap4 import IMAP4Client

import sys, getpass

class IMAPClient(IMAP4Client):
	def connectionMade(self):
		print "I have successfully connected to the server!"
		IMAPLogic(self)
		print "connectionMade returning."

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

		d.addCallback(self.loggedin)
		d.addCallback(self.stopreactor)

		print "IMAPLogic.__init__ returning."

	def loggedin(self, data):
		print "I'm logged in!"
		return self.logout()

	def logout(self):
		print "Logging out."
		d = self.proto.logout()
		return d

	def stopreactor(self, data = None):
		print "Stopping reactor."
		reactor.stop()

password = getpass.getpass("Enter password for %s on %s: " % (sys.argv[2], sys.argv[1]))

reactor.connectTCP(sys.argv[1], 143, IMAPFactory(sys.argv[2], password))
reactor.run()

