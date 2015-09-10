#!/usr/bin/env python

import xmlrpclib, sys, textwrap


class NewsCat:
	def __init__(self, catdata):
		self.id = catdata['id']
		self.title = catdata['title']

	def __cmp__(self, other):
		return cmp(self.title, other.title)

class NewsSource:
	def __init__(self, url = 'http://www.oreillynet.com/meerkat/xml-rpc/server.php'):
		self.s = xmlrpclib.ServerProxy(url)
		self.loadcats()

	def loadcats(self):
		print "Loading categories.."
		catdata = self.s.meerkat.getCategories()
		self.cats = [NewsCat(item) for item in catdata]
		self.cats.sort()


	def displaycats(self):
		numonline = 0
		i = 0
		for item in self.cats:
			sys.stdout.write("%2d: %20.20s " % (i + 1, item.title))
			i += 1
			numonline += 1
			if numonline % 3 == 0:
				sys.stdout.write("\n")

		if numonline != 0:
			sys.stdout.write("\n")


def promptcat(self):
	self.displaycats()
	sys.stdout.write("Select a ctegory or q to quit:")
	selection = sys.stdin.readline().strip()
	if selection == 'q':
		sys.exit(0)
	return int(selection) - 1

def dispcat(self, cat):
	items = self.s.meerkat.getItem({'category': cat,
					'ids': 1,
					'descriptions': 1,
					'categories': 1,
					'channels': 1,
					'dates': 1,
					'num_items': 15})
	if not len(items):
		print "Sorry, no items in that category."
		sys.stdout.write('Pross enter to continue:')
		sys.stdin.readline()
		return
	while 1:
		self.dispitemsummary(items)
		sys.stdout.write("Select story or q to qo to main menu: ")
		selection = sys.stdin.readline().strip()
		if selection == 'q':
			return
		self.dispitem(items[int(selection) - 1])

def dispitemsummary(self, items):
	counter = 0
	for item in items:
		print "%2d: %s" % (counter + 1, item['title'])
		counter += 1


def dispitem(self, item):
	print "--- %s ---" % item['title']
	print "Posted on", item['data']
	print "Descriptions:"
	print textwrap.fill(item['description'])
	print "\nLink:", item['link']
	sys.stdout.write("\nPress Enter to continue: ")
	sys.stdin.readline()

n = NewsSource()
while 1:
	cat = n.promptcat()
	n.dispcat(cat)

