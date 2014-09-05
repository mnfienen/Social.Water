import unittest
import tools
from tools import *

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
			''' LOGICNOTE: This should happen, so unless we hit the
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
		


if __name__ =='__main__':
	unittest.main()
