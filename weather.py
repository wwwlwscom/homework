#!/usr/bin/env python

from htmlentitydefs import entitydefs
from HTMLParser import HTMLParser

import sys, re, urllib2

interesting = ['Day Forecast for ZIP']

class WeatherParser(HTMLParser):
	def __init__(self):
		self.taglevels = []
		self.handledtags = ['title', 'table', 'tr', 'td', 'th']
		self.processing = None
		self.interestingtable = 0
		self.row = []
		HTMLParser.__init__(self)


	def handle_starttag(self, tag, attrs):
		if len(self.taglevels) and self.taglevels[-1] == tag:
			self.handle_endtag(tag)
		self.taglevels.append(tag)
		if tag == 'br':
			self.handle_data("<NEWLINE>")
		elif tag in self.handledtags:
			self.data = ''
			self.processing =tag

	def handle_data(self, data):
		if self.processing:
			self.data += data

	def handle_endtag(self, tag):
		if not tag in self.taglevels:
			return

		while len(self.taglevels):
			starttag = self.taglevels.pop()
			if starttag in self.handledtags:
				self.finishprocessing(starttag)
			if starttag == tag:
				break

	def cleanse(self):
		self.data = re.sub('(\s|\xa0)+', ' ', self.data)
		self.data = self.data.replace('<NEWLINE>', "\n").strip()


	def finishprocessing(self, tag):
		global interesting
		self.cleanse()
		if tag == 'title' and tag == self.processing:
			print " *** %s ***" % self.data
		elif (tag == 'td' or tag == 'th') and tag == self.processing:
			if not self.interestingtable:
				for item in interesting:
					if re.search(item, self.data, re.I):
						self.interestingtable = 1
						interesting = [x for x in interesting if x != item]
						print "\n *** %s\n" % self.data.strip()
						break
					else:
						self.row.append(self.data)
			elif tag == 'tr' and self.interestingtable:
				self.writerow()
				self.row = []
			elif tag == 'table':
				self.interestingtable = 0

			self.processing = None


	def writerow(self):
		cells = len(self.row)
		if cells < 2:
			return
		if cells > 2:
			width = (78 - cells) / cells
			maxwidth = width
		else:
			width = 20
			maxwidth = 58

		while [x for x in self.row if x != '']:
			for i in range(len(self.row)):
				thisline = self.row[i]
				if thisline.find("\n") != -1:
					(thisline, self.row[i]) = self.row[i].split("\n", 1)
				else:
					self.row[i] = ''
				thisline = thisline.strip()
				sys.stdout.write("%-*.*s " % (width, maxwidth, thisline))
			sys.stdout.write("\n")


	def handle_charref(self, name):
		try:
			charnum = int(name)
		except ValueError:
			return

		if charnum < 1 or charnum > 255:
			return
		self.handle_data(chr(charnum))

sys.stdout.write("Enter ZIP code:")
zip = sys.stdin.readline().strip()
url = "http://www.wunderground.com/cgi-bin/findweather/getForecast?query="+zip

req = urllib2.Request(url)
fd = urllib2.urlopen(req)

parser = WeatherParser()
data = fd.read()
data = re.sub('  ([^ =]+)=[^ ="]+="', ' \\1="', data)
data = re.sub('(?s)<!--.*?-->', '', data)
parser.feed(data)

		
