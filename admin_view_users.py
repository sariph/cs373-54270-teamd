import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminViewUsers(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.users = [i for i in db.GqlQuery("SELECT * FROM User")]

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'users': self.users,
		}
		path = os.path.join(os.path.dirname(__file__), 'adminViewUsers.html')
		self.response.out.write(template.render(path, template_values))

