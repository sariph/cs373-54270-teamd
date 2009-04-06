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
