#!usr/bin/python
import re

"""A bunch of tools for processing data from the newer Social.Water CrowdHydrology app.
@author Matthew G. McGovern 
@contact mgmcgove@buffalo.edu
@github github.com/mcgov
"""

ONE_LATLON = re.compile(r"\-?(?<![0-9])[0-9]{1,3}\.[0-9]{1,15}")

## Finds a lat/lon style point, between one and three leading digits,
##Up to 15 trailing digits. 
## TODO: This could be better if it searched more specifically...
## Maybe only searched for values within the proper ranges. -180,180 90,90


ONE_DOUBLE = re.compile(r"\-?(?<![0-9])[0-9]{1,15}\.[0-9]{1,15}")
## Searches for a double, between 1-15 leading digits, 1-15 trailing digits.
ALT_DOUBLE = re.compile(r"\-?(?<![0-9])[0-9]\.?[0-9]{0,10}[Ee][0-9]{1,10}")
## Searches for alternate scientific notation doubles, 1.23e200 or 1E20 or 1.2234E12300
## Must have 1 leading digit, may or may not have decimal digits in the significand,
## must have either e or E, and at least one expontential digit.

class NoLatLonError(Exception):
	def __init__(self,line):
		self.the_bad_line = line
	def __str__(self):
		return repr(self.the_bad_line)

def find_latlon(line):
	"""In a line of text, find the first double in that line of
	 text and return it (as a double).
	"""
	matches = ONE_LATLON.search(line)
	if matches:
		return float( matches.group(0) )

	else:
		raise NoLatLonError( line )
		"""Return the group if it has found a match. If not: raise our error."""

def find_double(line):
	"""In a line of text, find the first double in that line of
	 text and return it (as a double).
	"""
	matches = ONE_DOUBLE.search(line)
	if matches:
		return float( matches.group(0) )

	else:
		raise NoLatLonError( line )
		"""Return the group if it has found a match. If not: raise our error."""

