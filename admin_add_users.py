import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminAddUsers(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		validator = Validator(self.request.params.items())
		check = True
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break

		if check == True:
			new_user = User()
			for result in validator.results:
				if result['key'] == "comment_UTEID":
					new_user.UTEID = result['value']
				elif result['key'] == "comment_first_name":
					new_user.first_name = result['value']
				elif result['key'] == "optional_middle_name":
					new_user.middle_name = result['value']
				elif result['key'] == "comment_last_name":
					new_user.last_name = result['value']
				elif result['key'] == "comment_password":
					new_user.password= result['value']
				elif result['key'] == "phone_user":
					new_user.phone = db.PhoneNumber(result['value'])
				elif result['key'] == "email_user":
					new_user.email = db.Email(result['value'])
				elif result['key'] == "radio_position":
					new_user.position = result['value']

			if not self.UTEIDAlreadyExists(new_user.UTEID):
				new_user.put()
			else:
				result['valid'] = False

		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminAddUsers.html')
		self.response.out.write(template.render(path, template_values))

	def UTEIDAlreadyExists(self, name):
		try:
			check = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", name)
		except:
			return False

		if check.get() is None:
			return False
		else:
			return True

