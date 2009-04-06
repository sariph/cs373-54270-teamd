#!/usr/bin/env python

import unittest
import Validation
from validator import Validator

class TestAdmin (unittest.TestCase) :
	"""
	Test the Validator class
	"""
	def testvalidator1 (self) :
		form_data = [];
		#The first item in the tuple is the name of the field on the webpage
		#The second item is the value of the field
		#This is just checking if the validator class functions correctly
		#The individual validation functions are tested below
		form_data.append(('phone_applicant', '210-423-4243'))
		form_data.append(('email_applicant', 'flashki@hotmail.com'))
		form_data.append(('comment_major', 'Computer Science'))
		form_data.append(('comment_admission', '07-05-1988'))
		form_data.append(('comment_phd', 'PhD'))
		form_data.append(('comment_supervising', 'Downing'))
		form_data.append(('comment_citizen', 'citizen'))
		form_data.append(('comment_native', 'yes'))
		form_data.append(('comment_ta', 'no'))
		form_data.append(('comment_programming', 'C'))
		form_data.append(('comment_area', 'Algorithms'))
		form_data.append(('comment_qualified', 'Maybe'))
		form_data.append(('comment_wanted', 'You'))
		form_data.append(('comment_unwanted', 'Me'))
		form_data.append(('comment_native', 'yes'))
		form_data.append(('comment_specialization', 'None'))
		form_data.append(('comment_class_name', 'CS373'))
		form_data.append(('comment_inst_name', 'Downing'))
		form_data.append(('comment_exp_enrollment', '10'))
		form_data.append(('comment_num_ta_needed', '1'))
		form_data.append(('comment_num_ta_assigned', '0'))

		v = Validator(form_data)
		for r in v.results:
			if r['valid'] == False:
				print r['key'], r['value']
			self.assert_(r['valid'] == True)

	def testvalidator2 (self) :
		form_data = [];
		#The first item in the tuple is the name of the field on the webpage
		#The second item is the value of the field
		#This is just checking if the validator class functions correctly
		#The individual validation functions are tested below
		form_data.append(('phone_applicant', '210-423-42432'))
		form_data.append(('email_applicant', 'flashki@hotmail.com r23r'))
		form_data.append(('comment_major', ''))
		form_data.append(('comment_admission', '07-05-198'))
		form_data.append(('comment_phd', 'Ph'))
		form_data.append(('comment_supervising', ''))
		form_data.append(('comment_citizen', 'ht'))
		form_data.append(('comment_native', ''))
		form_data.append(('comment_ta', 'n'))
		form_data.append(('comment_programming', ''))
		form_data.append(('comment_area', ''))
		form_data.append(('comment_qualified', ''))
		form_data.append(('comment_wanted', ''))
		form_data.append(('comment_unwanted', ''))
		form_data.append(('comment_native', 'ye'))
		form_data.append(('comment_specialization', ''))
		form_data.append(('comment_class_name', ''))
		form_data.append(('comment_inst_name', ''))
		form_data.append(('comment_exp_enrollment', '10s'))
		form_data.append(('comment_num_ta_needed', '1d'))
		form_data.append(('comment_num_ta_assigned', ''))

		v = Validator(form_data)
		for r in v.results:
			if r['valid'] == True:
				print r['key'], r['value']
			self.assert_(r['valid'] == False)

	"""
	Test phone number validation.
	"""
	def testPhoneNumber1 (self) :
		self.assert_(not Validation.phone_number('abc'))
	def testPhoneNumber2 (self) :
		self.assert_(Validation.phone_number('123-4567'))
	def testPhoneNumber3 (self) :
		self.assert_(not Validation.phone_number('11-123-4567'))
	def testPhoneNumber4 (self) :
		self.assert_(Validation.phone_number('123-123-4567'))
	def testPhoneNumber5 (self) :
		self.assert_(not Validation.phone_number('123-45-67'))
	def testPhoneNumber6 (self) :
		self.assert_(not Validation.phone_number('123-4567-1'))

	"""
	Test phone number extension validation.
	"""
	def testphone_number_ext1 (self) :
		self.assert_(not Validation.phone_number_ext('abc'))
	def testphone_number_ext2 (self) :
		self.assert_(Validation.phone_number_ext(''))
	def testphone_number_ext3 (self) :
		self.assert_(Validation.phone_number_ext('11'))
	def testphone_number_ext4 (self) :
		self.assert_(Validation.phone_number_ext('11111'))

	"""
	Test e-mail validation.
	"""
	def testemail1 (self) :
		self.assert_(not Validation.email('abc'))
	def testemail2 (self) :
		self.assert_(not Validation.email('abc@11..com'))
	def testemail3 (self) :
		self.assert_(not Validation.email('abc..aa@asdf.com'))
	def testemail4 (self) :
		self.assert_(Validation.email('abc_asdf@adsfasd.org'))
	def testemail5 (self) :
		self.assert_(Validation.email('asdfasdf@cs.asdf.edu'))
	def testemail6 (self) :
		self.assert_(Validation.email('abc@asdf.asdf.asdf.asdf.asdf.com'))
	def testemail7 (self) :
		self.assert_(not Validation.email('.asdf@sdfsdaf.com'))
	def testemail8 (self) :
		self.assert_(not Validation.email('abc.@asdfasd.com'))
	def testemail9 (self) :
		self.assert_(Validation.email('-abc@asdfasd.com'))
	def testemail10 (self) :
		self.assert_(Validation.email('abc.aaa@asdfasd.com'))
	def testemail11 (self) :
		self.assert_(not Validation.email('ab c@asdfasd.com'))
	def testemail12 (self) :
		self.assert_(not Validation.email('ab#$c@asdfasd.com'))
	def testemail13 (self) :
		self.assert_(not Validation.email('ab@c@asdfasd.com'))

	"""
	Test date validation.
	"""
	def testdate1 (self) :
		self.assert_(not Validation.date('00-12-1999'))
	def testdate2 (self) :
		self.assert_(not Validation.date('02-30-1999'))
	def testdate3 (self) :
		self.assert_(not Validation.date('13-12-1999'))
	def testdate4 (self) :
		self.assert_(not Validation.date('01-00-1999'))
	def testdate5 (self) :
		self.assert_(Validation.date('02-28-1999'))
	def testdate6 (self) :
		self.assert_(not Validation.date('00-42-1999'))
	def testdate7 (self) :
		self.assert_(not Validation.date('00-12-99'))
	def testdate8 (self) :
		self.assert_(not Validation.date('00-00-12-1999'))
	def testdate9 (self) :
		self.assert_(not Validation.date('01-1-1999'))
	def testdate10 (self) :
		self.assert_(not Validation.date('5-12-1999'))
	def testdate11 (self) :
		self.assert_(not Validation.date('04-31-1999'))
	def testdate12 (self) :
		self.assert_(Validation.date('04-30-1999'))

	"""
	Test name validation.
	"""
	def testname1 (self) :
		self.assert_(not Validation.name('aaa'))
	def testname2 (self) :
		self.assert_(Validation.name('Aaa'))
	def testname3 (self) :
		self.assert_(Validation.name('Aaa-dd'))
	def testname4 (self) :
		self.assert_(not Validation.name('8aaa'))
	def testname5 (self) :
		self.assert_(not Validation.name(''))
	def testname6 (self) :
		self.assert_(not Validation.name('Baa--'))
	def testname7 (self) :
		self.assert_(not Validation.name('Aa$'))
	def testname8 (self) :
		self.assert_(not Validation.name('Ba a'))

	"""
	Test class number validation.
	"""
	def testclass_number1 (self) :
		self.assert_(not Validation.class_number('aaa'))
	def testclass_number2 (self) :
		self.assert_(not Validation.class_number('cs'))
	def testclass_number3 (self) :
		self.assert_(not Validation.class_number('cs1'))
	def testclass_number4 (self) :
		self.assert_(Validation.class_number('cs987'))
	def testclass_number5 (self) :
		self.assert_(Validation.class_number('CS987'))
	def testclass_number6 (self) :
		self.assert_(not Validation.class_number('cs*76'))
	def testclass_number7 (self) :
		self.assert_(not Validation.class_number('Cs333'))
	def testclass_number8 (self) :
		self.assert_(not Validation.class_number('cS123'))
	def testclass_number9 (self) :
		self.assert_(not Validation.class_number('ee315'))

	def testnumber1 (self) :
		self.assert_(not Validation.number('aaa'))
	def testnumber2 (self) :
		self.assert_(not Validation.number(''))
	def testnumber3 (self) :
		self.assert_(Validation.number('12312323'))


	"""
	Test comment validation.
	"""
	def testcomment1 (self) :
		self.assert_(Validation.comment('aaa'))

	"""
	Test degree validation.
	"""
	def testdegree1 (self) :
		self.assert_(not Validation.degree_type('aaa'))
	def testdegree2 (self) :
		self.assert_(not Validation.degree_type(''))
	def testdegree3 (self) :
		self.assert_(Validation.degree_type('PhD'))
	def testdegree4 (self) :
		self.assert_(Validation.degree_type('Masters'))

	"""
	Test citizen/resident validation.
	"""
	def testcitizen1 (self) :
		self.assert_(not Validation.citizen('aaa'))
	def testcitizen2 (self) :
		self.assert_(not Validation.citizen(''))
	def testcitizen3 (self) :
		self.assert_( Validation.citizen('citizen'))
	def testcitizen4 (self) :
		self.assert_(Validation.citizen('resident'))

	"""
	Test yes/no validation.
	"""
	def testyesno1 (self) :
		self.assert_(not Validation.yes_no('aaa'))
	def testyesno2 (self) :
		self.assert_(Validation.yes_no('yes'))
	def testyesno3 (self) :
		self.assert_(Validation.yes_no('no'))
	def testyesno4 (self) :
		self.assert_(not Validation.yes_no(''))

	"""
	Test empty validation
	"""
	def testempty1 (self) :
		self.assert_(not Validation.empty("a"))
	def testempty2 (self) :
		self.assert_(not Validation.empty("12345"))
	def testempty3 (self) :
		self.assert_(not Validation.empty("!@$"))
	def testempty4 (self) :
		self.assert_(Validation.empty(""))

	"""
	Test semester validation
	"""
	def testsemester1 (self) :
		self.assert_(Validation.validSemester("Spring"))
	def testsemester2 (self) :
		self.assert_(Validation.validSemester("Summer"))
	def testsemester3 (self) :
		self.assert_(Validation.validSemester("Fall"))
	def testsemester4 (self) :
		self.assert_(not Validation.validSemester("4321780"))
	def testsemester5 (self) :
		self.assert_(not Validation.validSemester(""))

	"""
	Test year validation
	"""
	def testyear1 (self) :
		self.assert_(Validation.validYear("1999"))
	def testyear2 (self) :
		self.assert_(Validation.validYear("2009"))
	def testyear3 (self) :
		self.assert_(not Validation.validYear("1823"))
	def testyear4 (self) :
		self.assert_(not Validation.validYear("2011"))
	def testyear5 (self) :
		self.assert_(not Validation.validYear("99"))

	"""
	Test enrollment validation
	"""
	def testenrollment1 (self) :
		self.assert_(Validation.validExpectedEnrollment("0"))
	def testenrollment2 (self) :
		self.assert_(Validation.validExpectedEnrollment("10000000000"))
	def testenrollment3 (self) :
		self.assert_(not Validation.validExpectedEnrollment("five"))
	def testenrollment4 (self) :
		self.assert_(not Validation.validExpectedEnrollment("afeh"))
	def testenrollment5 (self) :
		self.assert_(not Validation.validExpectedEnrollment(""))

if __name__ == "__main__" :
	unittest.main()
