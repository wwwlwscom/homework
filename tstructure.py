#!/usr/bin/env python


from twisted.internet import defer, reactor, protocol
from twisted.mail.imap4 import IMAP4Client
import sys, email, getpass

class IMAPClient(IMAP4Client):
	def connectionMade(self):
		IMAPLogic(self)


class IMAPFactory(protocol.ClientFactory):
	protocol = IMAPClient
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def clentConnectionFailed(self, connector, reason):
		print "Client connection failed:", reasion
		reactor.stop()

class IMAPLogic:
	def __init__(self, proto):
		self.proto = proto
		self.factory = proto.factory

		d = self.proto.login(self.factory.username, self.factory.password)
		d.addCallback(lambda x: self.proto.examine('INBOX'))
		d.addCallback(lambda x: self.downloadinfo())
		d.addCallback(self.displayinfo)
		d.addCallback(self.logout)
		d.addCallback(self.stopreactor)

		d.addErrback(self.errorhappened)

	def downloadinfo(self):
		dstructure = self.proto.fetchSimplifiedBody('1:*', uid = 1)
		denvelope = self.proto.fetchEnvelope('1:*', uid = 1)
		return defer.DeferredList([dstructure, denvelope])

	def displayinfo(self, data):
		structure, envelope = data
		for msgnum, structdata in structure[1].items():
			envelopedata = envelope[1][msgnum]['ENVELOPE']
			print "Message %s (%s): %s" % (msgnum, structdata['UID'], envelopedata[1])
			parts = structdata['BODY']
			self.printpart(parts)

	def printpart(self, part, itemnum = '1', istoplevel = 1):
		if not istoplevel:
			nextitem = itemnum + ' .1'
		else:
			nextitem = itemnum 
		
		if not isinstance(part[0], str):
			for item in part[:-1]:
				self.printpart(item, nextitem, 0)
				cparts = nextitem.split('.')
				cparts[-1] = str(int(cparts[-1]) + 1)
				nextitem = '.'.join(cparts)
		else:
			print "%s: %s/%s" % (itemnum, part[0], part[1])
			if part[0].lower() == 'message' and part[1].lower() == 'rfc822':
				self.printpart(part[8], nextitem, 0)

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
