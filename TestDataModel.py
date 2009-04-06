#!/usr/bin/env python

import unittest
import Validation
import DataModels
from validator import Validator

class Test (unittest.TestCase) :
	"""
	Test database model
	"""
	def testUser1 (self) :
		u = DataModels.User()
		u.UTEID = "fafea"
		u.first_name = "fa"
		u.last_name = "fea"
		u.middle_name = ""
		u.password = "3r8yu9f"
		u.phone = "123-456-7890"
		u.email = "fafea@utexas.edu"
		u.position = "Undergraduate"
		self.assert_(Validation.UserDataValidator(u))

	def testUser2 (self) :
		u = DataModels.User()
		u.UTEID = "fafea"
		u.first_name = "fa"
		u.last_name = "fea"
		u.middle_name = ""
		u.password = "3r8yu9f"
		u.phone = "123-456-7890"
		u.email = "fafea@utexas.edu"
		u.position = "Undergraduate"
		self.assert_(Validation.UserDataValidator(u))

	def testUser3 (self) :
		u = DataModels.User()
		u.UTEID = "fafea"
		u.first_name = "fa"
		u.last_name = "fea"
		u.middle_name = ""
		u.password = "3r8yu9f"
		u.phone = "123-456-7890"
		u.email = "fafea@utexas.edu"
		u.position = "Undergraduate"
		self.assert_(Validation.UserDataValidator(u))


if __name__ == "__main__" :
	unittest.main()
