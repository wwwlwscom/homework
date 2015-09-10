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
		self.logintries = 1
		
		d = self.login()
		
		d.addCallback(self.loggedin)
		d.addErrback(self.loginerror)
		d.addCallback(self.stopreactor)
		d.addCallback(self.stopreactor)

		d.addErrback(self.stopreactor)

		print "IMAPLogic.__init__ returning."
	
	def login(self):
		print "Logging in ..."
		return self.proto.login(self.factory.username, self.factory.password)

	def loggedin(self, data):
		print "I'm logged in!"

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

	def loginerror(self, failure):
		print "Your login failed (attempt %d) ." % self.logintries
		if self.logintries >= 3:
			print "You have tried to log in three times; I'm giving up."
			return failure
		self.logintries += 1

		sys.stdout.write("New username:")
		self.factory.username = sys.stdin.readline().strip()
		self.factory.password = getpass.getpass("New password:")

		d = self.login()
		d.addErrback(self.loginerror)
		return d

password = getpass.getpass("Enter password for %s on %s: " % (sys.argv[2], sys.argv[1]))

reactor.connectTCP(sys.argv[1], 143, IMAPFactory(sys.argv[2], password))
reactor.run()

