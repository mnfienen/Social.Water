import unittest
import tools
from tools import *
import utils
import social_water as sw


class email_stub():
    def __init__(self):
        self.header = "sms from (504) 908-0034 test header"

class dummyObj():
    def __init__(self):
        self.usr = None
        self.pwd_encoded = "ABCD"
        self.email_scope = "ALL"
        self.stations_and_bounds = dict()
        self.std_time_utc_offset = 0
        self.dst_time_utc_offset = 0
        self.minstatnum = 0
        self.maxstatnum = 0


class TestTools(unittest.TestCase):
    def setUp(self):
        self.double1 = 123.456788
        self.double2 = -32.3454632123
        self.line = "Here's a line of test text" + str(self.double1) + ":$:" + str(self.double2)

    def test_inpardata_creation(self):
        test = sw.inpardata("testfile.xml")

    def test_find_decimal1(self):
        self.assertEqual(tools.find_decimal(str(self.double1)), self.double1)

    def test_find_decimal2(self):
        self.assertEqual(tools.find_decimal(str(self.double2)), self.double2)

    def test_find_decimal3(self):
        thedouble = "-9000.0000"
        try:
            thedouble = tools.find_decimal(thedouble)
            self.fail("No error was thrown while parsing an invalid double" + thedouble)
        except NoNumError as error:
            return


    def test_find_decimal4(self):
        thedouble = "2040"
        try:
            thedouble = tools.find_decimal(thedouble)
            self.fail("No error was thrown while parsing an invalid number " + thedouble)
        except NoNumError as error:
            return


    def test_find_decimal_in_text(self):
        self.assertEqual(tools.find_decimal(self.line), self.double1)

    def test_asciidammit(self):
        tester = "Here's a string to test! Wooooooop\r\n\t"
        tester = utils.asciidammit(tester)
        self.assertEqual(tester, str(tester))

        # #this does baiscally nothing now, obviously...

    ##There have to be some weird cases where things can get funky though. TODO: this should check for those!

    def test_remove_punctuation(self):
        tester = "-,.:"
        tester = utils.remove_punctuation(tester)
        self.assertTrue(tester == "    ")

    def test_remove_cr(self):
        tester = "Here's some text that looks like it's windows formatted \n\r"
        tester = utils.remove_cr(tester)
        self.assertEqual(tester, "Here's some text that looks like it's windows formatted \n ")

    def test_validate_strings(self):
        tester = None
        self.assertTrue(not utils.validate_string(tester))
        tester = ""
        self.assertTrue(not utils.validate_string(tester))
        tester = 0.00123
        self.assertTrue(not utils.validate_string(tester))
        tester = 999999999999999999999999999999999
        self.assertTrue(not utils.validate_string(tester))
        tester = 'a'
        self.assertTrue(utils.validate_string(tester))
        tester = "This is a perfectly valid string"
        self.assertTrue(utils.validate_string(tester))
        tester = "This \n\ris \n\r\ra \n\r\t\033[49m\n \033[31mperfectly\033[39m \r\nvalid string"
        self.assertTrue(utils.validate_string(tester))

    def test_correct_subject(self):

        tester = "sms from 120341"
        self.assertEqual(utils.correct_subject(tester), True)

        tester = "SMS FROM 120341"
        self.assertEqual(utils.correct_subject(tester), True)

        tester = "S M S F R O M 123-8121-0412"
        self.assertTrue(not utils.correct_subject(tester), "Spaces in line, shouldn't have parsed as true")

        tester = "Organisms from the bottom of the sea"
        self.assertTrue(utils.correct_subject(tester), "This will parse as true but probably shouldn't...")

        tester = "BACK SPASMS FROM WORK RELATED INJURIES? CALL SUPERLAWER AT 1800SCAMLAW NOW!"
        self.assertTrue(utils.correct_subject(tester), "This will parse as true but probably shouldn't...")


    def test_find_phone_no_country_code(self):
        line = "Some phone number: (504) 908-0034 "
        self.assertEqual(tools.find_phone_number(line), "(504) 908-0034")


    def test_find_phone_with_country_code3(self):
        """

        """
        line = "Some phone number: 3223-504-908-0034 "
        try:
            thing = tools.find_phone_number(line)
            self.fail(" 3223-504-908-0034 shouldn't have parsed as a phone number.")
        except NoNumError as error:

            pass

    def test_find_phone_with_dash(self):
        line = "Some phone number: -(504) 908-0034 "
        try:
            thing = tools.find_phone_number(line)
            self.fail("-(504) 908-0034 shouldn't have parsed as a phone number.")
        except NoNumError as error:

            pass

    def test_find_phone_with_incomplete_entry(self):
        line = "Some phone number: 04-908-0034 "
        try:
            thing = tools.find_phone_number(line)
            self.fail("04-908-0034 shouldn't have parsed as a phone number.")
        except NoNumError as error:
            ##Woo! it worked.
            pass

    """
    def test_find_phone_with_parens(self):
        line = "Some phone number: (504)-908-0034 "
        try:
            thing  = tools.find_phone_number(line)
        except NoNumError as error:
            self.fail("(504)-908-0034 should have parsed as a number.")
            pass

    def test_find_phone_with_parens2(self):
        line = "Some phone number: (504) 908-0034 "
        try:
            thing  = tools.find_phone_number(line)
        except NoNumError as error:
            self.fail(" (504) 908-0034 should have parsed as an accceptable number." )
            pass
    """

    def test_find_phone_with_spaces_and_dashes(self):
        line = "Some phone number: (504) 908-0034 "
        try:
            thing = tools.find_phone_number(line)
        except NoNumError as error:
            self.fail(" (504) 908-0034 should have parsed as an accceptable number.")
            pass

    def test_find_phone_with_spaces_and_dashes2(self):
        line = "SMS from (585) 370-7180 "
        try:
            thing = tools.find_phone_number(line)
        except NoNumError as error:
            self.fail(" (504) 908-0034 should have parsed as an accceptable number.")
            pass


    def test_remove_chars(self):
        string = "Here's a string and we will remove () some ';. chars"
        string = remove_chars(string, "'()';.")
        self.assertEqual(string, "Heres a string and we will remove  some  chars")
        string = "      woo        "
        string = remove_chars(string, "o ")
        self.assertEqual(string, "w")

    def test_hash_phone_number(self):
        testmsg = email_stub()
        testhash = hash_phone_number(testmsg)
        self.assertEqual(str(testhash), "9d6feecd-8c04-3264-926e-3da1476e4125")

    def test_find_double(self):
        testmsg1 = "Some nonsense and then 2344.234e12 let's hope that works."
        testmsg2 = None
        try:
            testmsg2 = find_double(testmsg1)
        except NoNumError:
            print(testmsg2)
            self.fail("No float value was found in the line: " + testmsg1)
        else:
            self.assertEqual(testmsg2, float("2344234000000000.0"))
        #huzzah!

    def test_find_double2(self):
        testmsg1 = "Some nonsense and then 2344.234234 let's hope that works."
        testmsg2 = None
        try:
            testmsg2 = find_double(testmsg1)
        except NoNumError:
            print(testmsg2)
            self.fail("No float value was found in the line: " + testmsg1)
        else:
            self.assertEqual(testmsg2, float("2344.234234"))
        #huzzah!

    def test_find_double3(self):
        testmsg1 = "Some nonsense and then 12.00E2 let's hope that works."
        testmsg2 = None
        try:
            testmsg2 = find_double(testmsg1)
        except NoNumError:
            print(testmsg2)
            self.fail("No float value was found in the line: " + testmsg1)
        else:
            self.assertEqual(testmsg2, float("1200"))
        #huzzah!

    def test_find_double4(self):
        testmsg1 = "Some nonsense and then 12E2 let's hope that works."
        testmsg2 = None
        try:
            testmsg2 = find_double(testmsg1)
        except NoNumError:
            pass
        else:
            self.assertEqual(testmsg2, float("1200"))
        #huzzah!

    def test_find_double5(self):
        testmsg1 = "Some nonsense and then .5 let's hope that works."
        testmsg2 = None
        try:
            testmsg2 = find_double(testmsg1)
        except NoNumError:
            print(testmsg2)
            self.fail("No float value was found in the line: " + testmsg1)
        else:
            self.assertEqual(testmsg2, .5)
        #huzzah!

    def test_find_fraction(self):
        msg = "The water level is 3 3/4 inches"
        try:
            parsed = find_fraction(msg)
        except NoNumError:
            self.fail("No Fraction Found in " + msg)
        else:
            self.assertEqual(parsed, 3.75)

    def test_find_fraction2(self):
        msg = "The water level is 12 2/3 inches"
        try:
            parsed = find_fraction(msg)
        except NoNumError:
            self.fail("No Fraction Found in " + msg)
        else:
            self.assertEqual(parsed, 12.0 + (2 / 3.0))

    def test_find_fraction3(self):
        msg = "The water level is 1/2 inch"
        try:
            parsed = find_fraction(msg)
        except NoNumError:
            self.fail("No Fraction Found in " + msg)
        else:
            self.assertEqual(parsed, .5)

    def test_find_fraction6(self):
        msg = "The water level is 1/2 inch"
        try:
            parsed = find_fraction(msg)
        except NoNumError:
            self.fail("No Fraction Found in " + msg)
        else:
            self.assertEqual(parsed, .5)


    def test_yank_or_log(self):
        """
        Set up an emailreeader with some dummy params and test the bad contribution logging on a dummy message.
        TODO: this needs to be expanded and test a lot more conditions.
        :return:
        """
        dummyparams = dummyObj()
        msgstub = sw.email_reader(dummyparams)

        msg = sw.email_message
        msg.station_line = "NY1001"
        msg.fromUUID = "ea5c7fb3-e651-3257-9b9e-4e0dc5fd4d9a"
        msg.header = "sms from AABBCCDD"
        msg.body = "NY1001 3.25"
        msg.date = "2015"
        msgstub.extract_gauge_info(msg)
        #print msgstub.totals["AABBCCDD"]
        self.assertTrue( msgstub.totals["ea5c7fb3-e651-3257-9b9e-4e0dc5fd4d9a"] == ('2015', 1, 0) )
        msgstub.extract_gauge_info(msg)
        self.assertTrue( msgstub.totals["ea5c7fb3-e651-3257-9b9e-4e0dc5fd4d9a"] == ('2015', 2, 0) )
        ##print msgstub.totals["ea5c7fb3-e651-3257-9b9e-4e0dc5fd4d9a"]
        msg.body = "NY1001    "
        msgstub.extract_gauge_info(msg)
        #print msgstub.totals["AABBCCDD"]
        self.assertTrue( msgstub.totals["ea5c7fb3-e651-3257-9b9e-4e0dc5fd4d9a"] == ('2015', 3, 1) )



    def test_robot_email_creation(self):
        test_email = sw.email_message("09211908","sms_from 1 555-908-0812","IMAROBOT,NY20002,123,54.09")
        self.assertTrue(test_email.robot_status )



if __name__ == '__main__':
    print("\033[34mSocial.Water Test Suite\033[39m")
    print("\033[32mRunning tests now...\033[39m")
    unittest.main()
