import unittest
import tools
from tools import *
import utils

class TestTools(unittest.TestCase):

	def setUp(self):
		self.double1 = 123.456788
		self.double2 = -32.3454632123
		self.line = "Here's a line of test text" + str(self.double1) + ":$:" +str(self.double2)


	def test_find_latlon1(self):
		self.assertEquals(tools.find_latlon(str(self.double1)), self.double1  )

	def test_find_latlon2(self):
		self.assertEquals(tools.find_latlon(str(self.double2)), self.double2  )

	def test_find_latlon3(self):
		thistest= "-9000.0000"
		try:
			thedouble = tools.find_latlon(thistest)
			self.fail("No error was thrown while parsing an invalic double")
		except NoLatLonError as error:
			#print "We didn't parse the double" ##Good, this worked!
			pass 
			''' LOGIC NOTE: This should happen, so unless we hit the
			 else,it should just do nothing and this
			 will count as a win.'''
		else:
			#If we get here, an exception was not raised!
			## Fail! fail like a sophomore!
			self.fail("The following value should not have parsed as a double: " + thedouble )

	
	def test_find_latlon4(self):
		thistest= "2040"
		try:
			thedouble = tools.find_latlon(thistest)
			self.fail("No error was thrown while parsing an invalic number " + thistest)
		except NoLatLonError as error:
			#print "We didn't parse the double" ##Good, this worked!
			pass 
			''' LOGICNOTE: This should happen, so unless we hit the
			 else,it should just do nothing and this
			 will count as a win.'''
		else:
			#If we get here, an exception was not raised!
			## Fail! fail like a sophomore!
			self.fail("The following value should not have parsed as a double: " + thedouble )
	
	def test_find_latlon_in_text(self):
		self.assertEquals(tools.find_latlon(self.line), self.double1  )
		
	def test_asciidammit(self):
		tester = "Here's a string to test! Wooooooop\r\n\t"
		tester = utils.asciidammit(tester)
		self.assertEquals(tester, unicode(tester))
		##this does baiscally nothing now, obviously...
		##There have to be some weird cases where things can get funky though. TODO: this should check for those!

	def test_remove_punctuation(self):
		tester = "-,.:"
		tester = utils.remove_punctuation(tester)
		self.assertTrue(tester == "    " )

	def test_remove_cr(self):
		tester = "Here's some text that looks like it's windows formatted \n\r"
		tester = utils.remove_cr(tester)
		self.assertEquals(tester, "Here's some text that looks like it's windows formatted \n ")

	def test_validate_strings(self):
		tester = None
		self.assertTrue( not utils.validate_string(tester) )
		tester = ""
		self.assertTrue( not utils.validate_string(tester) )
		tester = 0.00123
		self.assertTrue( not utils.validate_string(tester) )
		tester = 999999999999999999999999999999999L
		self.assertTrue( not utils.validate_string(tester) )
		tester = 'a'
		self.assertTrue( utils.validate_string(tester) )
		tester = "This is a perfectly valid string"
		self.assertTrue( utils.validate_string(tester) )
		tester = "This \n\ris \n\r\ra \n\r\t\033[49m\n \033[31mperfectly\033[39m \r\nvalid string"
		self.assertTrue( utils.validate_string(tester) ) 








if __name__ =='__main__':
	print "\033[34mSocial.Water Test Suite\033[39m"
	print "\033[32mRunning tests now...\033[39m"
	unittest.main()
