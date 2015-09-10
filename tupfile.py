#!/usr/bin/env python

from twisted.internet import defer, reactor, protocol
from twisted.mail.imap4 import IMAP4Client
from StringIO import StringIO
import sys, getpass, email

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
		d.addCallback(self.upload)
		d.addCallback(self.logout)
		d.addCallback(self.stopreactor)

		d.addErrback(self.errorhappened)

	def upload(self, data = None):
		fd = open(sys.argv[3])
		content = fd.read()
		fd.close()

		content = "\r\n".join(content.splitlines()) + "\r\n"

		fakefd = StringIO(content)
		return self.proto.append('INBOX', fakefd)

	def logout(self, data = None):
		return self.proto.logout()

	def stopreactor(self, data = None):
		reactor.stop()

	def errorhappened(self, failure):
		print "An error occurred:", failure.getErrorMessage()
		d = self.logout()
		d.addBoth(self.stopreactor)
		return failure

password = getpass.getpass("Enter password for %s on %s: " % (sys.argv[2], sys.argv[1]))
reactor.connectTCP(sys.argv[1], 143, IMAPFactory(sys.argv[2], password))
reactor.run()


