#!usr/bin/python
import re
import hashlib
import uuid
import base64


"""A bunch of tools for processing data from the newer Social.Water CrowdHydrology app.
@author Matthew G. McGovern 
@contact mgmcgove@buffalo.edu
@github github.com/mcgov
"""

ONE_DECIMAL = re.compile(r"\-?(?<![0-9])[0-9]{1,3}\.[0-9]{1,15}")

A_PHONE_NUMBER = re.compile(r"(?<!\-)(?<![0-9])\([0-9]{3}\) [0-9]{3}\-[0-9]{4}")
## Finds a double/float style number, between one and three leading digits,


ONE_DOUBLE = re.compile(r"\-?(?<![0-9])([0-9]{1,15})?\.[0-9]{1,15}([eE][+-]?[0-9]{1,15})?")
## Searches for a double, between 1-15 leading digits, 1-15 trailing digits.
##This regex will also match a float of form 90.2342342234e12412.
## The digits are limited to 15 simply to avoid a possible stack overflow while searching through a *really* large number string.
## Out in the field, there shouldn't be any floats with 45 significant digits, so if we get to that point then something has gone really wrong.

FRACTION_FINDER = re.compile(r"([0-9]{0,9}(?<=[0-9]) )?[0-9]{0,9}[/\\][0-9]{0,9}")

class NoNumError(Exception):
	def __init__(self,line):
		self.the_bad_line = line
	def __str__(self):
		return repr(self.the_bad_line)

def find_fraction(line):
	"""In a line of text, find any fractional values reported in that text.
	"""
	matches = FRACTION_FINDER.search(line)
	if matches:
		match = matches.group(0)
		fraction = None
		## We're matching some different kinds of fractions.
		##If the fraction if preceded by an integer value, we follow this branch:
		if ' ' in match:
			#the regex should only match a space if an 
			##integer before the fraction was found.
			splits = match.split(' ')
			if '\\' in splits[1]: ##depending on the slash type...
				fraction = splits[1].split('\\')
			elif '/' in splits[1]: ## split things up
				fraction = splits[1].split('/') 
			else: ## parse that number and combine the elements into one float!
				raise NoNumError( "Something went super wrong with the processing of a fractional value!" + match)
			thenum = float( splits[0] ) + float( fraction[0] ) / float( fraction[1] )  
			return thenum
		else:
			## otherwise just parse the fraction, since it should be by itself.
			if '\\' in match:
				fraction = match.split('\\')
			elif '/' in match:
				fraction = match.split('/') 
			else:
				raise NoNumError( "Something went super wrong with the processing of a fractional value!" + match)
			thenum =  float( fraction[0] ) / float( fraction[1] )  
		return thenum
	else:
		raise NoNumError( line )
		"""Return the group if it has found a match. If not: raise our error."""


def find_decimal(line):
	"""In a line of text, find the first double in that line of
	 text and return it (as a double).
	"""
	matches = ONE_DECIMAL.search(line)
	if matches:
		return float( matches.group(0) )

	else:
		raise NoNumError( line )
		"""Return the group if it has found a match. If not: raise our error."""

def find_double(line):
	"""In a line of text, find the first double in that line of
	 text and return it (as a double).
	"""
	matches = ONE_DOUBLE.search(line)
	if matches:
		return float( matches.group(0) )

	else:
		raise NoNumError( line )
		"""Return the group if it has found a match. If not: raise our error."""

def find_phone_number(line):
	matches = A_PHONE_NUMBER.search(line)
	if matches:
		return str( matches.group(0) )
	else:
		raise NoNumError( line )
	"""Pretty similar to these other functions. If we find a number return it, otherwise spit back the line and raise an exception."""

def remove_chars(string,charstoremove):
	for char in charstoremove:
		string = string.replace(char, '')
	string.strip() #gets rid of nulls on the ends
	return string

def hash_phone_number(email_message):
	##This will take a message object and generate a UUID.
	##I want to make sure that things don't vary too much,
	##  and that phone numbers are consistently related to the same UUID.
	identifier = None
	identifier = find_phone_number(email_message.header )
	identifier = remove_chars(identifier, "()- ") #remove all the chars in the second string 
	hasher = uuid.uuid3( uuid.NAMESPACE_OID, identifier )
	## There is a vulnerability where this identifier should first be 'salted' before hashed.
	## This is to prevent people from just stealing the whole list and iterating through
	## all possible phone numbers to deanonymize the data.
	## I'm not sure if this is really a problem with our data, since this is all pretty unsensitive.
	return hasher 

def hash_number(header):
	identifier = find_phone_number(header )
	identifier = remove_chars(identifier, "()- ") #remove all the chars in the second string 
	hasher = uuid.uuid3( uuid.NAMESPACE_OID, identifier )
	## There is a vulnerability where this identifier should first be 'salted' before hashed.
	## This is to prevent people from just stealing the whole list and iterating through
	## all possible phone numbers to deanonymize the data.
	## I'm not sure if this is really a problem with our data, since this is all pretty unsensitive.
	return hasher 

def log_bad_contribution(email_message, reader):

	number = str( email_message.header )
	remove_chars(number, "()- SMfrom")
	hasher = uuid.uuid3( uuid.NAMESPACE_OID, number ) 
	userid = ( str(hasher) )
	if userid in reader.totals:
		reader.totals[userid] = ( reader.totals[userid][0], reader.totals[userid][1]+1, reader.totals[userid][2] + 1 )
		
	else:
		reader.totals[userid] = ( email_message.date , 1, 1 )
	
	print reader.totals[userid]