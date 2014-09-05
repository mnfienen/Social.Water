#!usr/bin/python
import re

"""A bunch of tools for processing data from the newer Social.Water CrowdHydrology app.
@author Matthew G. McGovern 
@contact mgmcgove@buffalo.edu
@github github.com/mcgov
"""

ONE_DOUBLE = re.compile(r"\-?(?<![0-9])[0-9]{1,3}\.[0-9]{1,15}")

class NoDoubleError(Exception):
	def __init__(self,line):
		self.the_bad_line = line
	def __str__(self):
		return repr(self.the_bad_line)

def find_double(line):
	"""In a line of text, find the first double in that line of
	 text and return it (as a double).
	"""
	matches = ONE_DOUBLE.search(line)
	if matches:
		return float( matches.group(0) )

	else:
		raise NoDoubleError( line )
		"""Return the group if it has found a match. If not: raise our error."""


