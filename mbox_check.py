"""
	mbox_check.py - A mbox/maildir checker 

	Copyright 2006 Kenneth Hayber <ken@hayber.us>,
	All rights reserved.
"""

import mailbox, re
import os

from checker import Checker
class MBOXChecker(Checker):
	def __init__(self, config=None):
		Checker.__init__(self, config)
		self.protocol = 'MBOX'
		try:
			self.filename = config['filename']
		except:
			self.filename = os.getenv('MAIL', 'none')

	def check(self):
		count = 0
		seen = 0
	
		try:
			file = open(self.filename, "r")
		except:
			self.blocker.trigger()
			return
	
		for line in file.xreadlines():
			if re.search("^From (\S*) ", line):
				count += 1
			if re.search("^Status:.*R.*", line):
				seen += 1
			yield None

		self.unseen = count - seen
		if self.unseen > 0:
			self.results = "%s (%d/%d)\n" % (self.name, self.unseen, count)
		else:
			self.results = ""

		file.close()
		self.blocker.trigger()
