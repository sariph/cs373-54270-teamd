#!/usr/bin/env python

import unittest
import Validation
from DataModels import *
from validator import Validator

class Test () :
	"""
	Test database model
	"""
	def start (self) :
		"""
		Displays the class template upon get request.
		"""
		self.results = []
		self.results.append(self.testUser1())
		self.results.append(self.testUser2())
		self.results.append(self.testUser3())
		self.results.append(self.testUser4())
		self.results.append(self.testTA1())
		self.results.append(self.testTA2())
		self.results.append(self.testInstructor1())
		self.results.append(self.testInstructor2())
		self.results.append(self.testInstructor_App1())
		self.results.append(self.testInstructor_App2())
		self.results.append(self.testApplicant1())

	def testUser1 (self) :
		u = User()
		u.UTEID = "fafea"
		u.first_name = "Fa"
		u.last_name = "Fea"
		u.middle_name = "Afes"
		u.password = "3r8yu9f"
		u.phone = "123-456-7890"
		u.email = "fafea@utexas.edu"
		u.position = "Undergraduate"
		print "testUser1 =",Validation.UserDataValidator(u)

	def testUser2 (self) :
		u = User()
		u.UTEID = "bob"
		u.first_name = "Bob"
		u.last_name = "Billy"
		u.middle_name = ""
		u.password = "hotstuff"
		u.phone = "555-123-4500"
		u.email = "hotmale@hotmail.com"
		u.position = "Graduate"
		print "testUser2 =",Validation.UserDataValidator(u)

	def testUser3 (self) :
		u = User()
		u.UTEID = "jj"
		u.first_name = "Jenny"
		u.last_name = "Johnson"
		u.middle_name = ""
		u.password = "<3"
		u.phone = "512-867-5309"
		u.email = "jenny@onthewall.com"
		u.position = "Professor"
		print "testUser3 =",Validation.UserDataValidator(u)

	def testUser4 (self) :
		u = User()
		u.UTEID = "jj"
		u.first_name = "jenny"
		u.last_name = "johnson"
		u.middle_name = ""
		u.password = "<3"
		u.phone = "512-867-5309"
		u.email = "jenny@onthewall.com"
		u.position = "Professor"
		print "testUser4 =",Validation.UserDataValidator(u)

	def testTA1 (self) :
		ta = TA()
		ta.UTEID = "ab"
		ta.class_id = "cs123"
		print "testTA1 =",Validation.TADataValidator(ta)

	def testTA2 (self) :
		ta = TA()
		ta.UTEID = "ab"
		ta.class_id = "19809409432098"
		print "testTA2 =",Validation.TADataValidator(ta)

	def testInstructor1 (self) :
		i = Instructor()
		i.UTEID = "i"
		i.class_id = "cs445"
		print "testInstructor1 =",Validation.InstructorDataValidator(i)

	def testInstructor2 (self) :
		i = Instructor()
		i.UTEID = ""
		i.class_id = "cs445"
		print "testInstructor2 =",Validation.InstructorDataValidator(i)

	def testInstructor_App1 (self) :
		i = Instructor_App()
		i.UTEID = "i"
		i.class_id = "cs445"
		print "testInstructor_App1 =",Validation.InstructorApplicantDataValidator(i)

	def testInstructor_App2 (self) :
		i = Instructor_App()
		i.UTEID = ""
		i.class_id = "cs445"
		print "testInstructor_App2 =",Validation.InstructorApplicantDataValidator(i)

	def testApplicant1 (self) :
		a = Applicant()
		a.UTEID = "fafea"
		a.major = "sleeping"
		a.admission = "03-12-2008"
		a.degree = "PhD"
		a.supervisor = "dad"
		a.citizenship = "Resident"
		a.native_english = "Yes"
		a.history_comment = "fdsa"
		a.programming_comment = "fdsa"
		a.specialization_comment = "fdsa"
		a.qualified_comment = "fdsa"
		print "testApplicant1 =",Validation.ApplicantDataValidator(a)
