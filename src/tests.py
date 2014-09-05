import unittest
import tools
from tools import *
class TestTools(unittest.TestCase):

	def setUp(self):
		self.double1 = 123.456788
		self.double2 = -32.3454632123
		self.line = "Here's a line of test text" + str(self.double1) + ":$:" +str(self.double2)


	def test_find_double1(self):
		self.assertEquals(tools.find_double(str(self.double1)), self.double1  )

	def test_find_double2(self):
		self.assertEquals(tools.find_double(str(self.double2)), self.double2  )

	def test_find_double3(self):
		thistest= "-9000.0000"
		try:
			thedouble = tools.find_double(thistest)
		except NoDoubleError as error:
			#print "We didn't parse the double" ##Good, this worked!
			pass 
			''' LOGICNOTE: This should happen, so unless we hit the
			 else,it should just do nothing and this
			 will count as a win.'''
		else:
			#If we get here, an exception was not raised!
			## Fail! fail like a sophomore!
			self.fail("The following value should not have parsed as a double: " + thedouble )


if __name__ =='__main__':
	unittest.main()
