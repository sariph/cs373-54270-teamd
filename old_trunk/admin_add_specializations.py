import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminAddSpecializations(webapp.RequestHandler):
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
			for result in validator.results:
				if not self.SpecializationAlreadyExists(result['value']):
						specialization = Specialization(specialization=result['value'])
						specialization.put()
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
			'specializations': [i for i in db.GqlQuery("SELECT * FROM Specialization")],
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminAddSpecializations.html')
		self.response.out.write(template.render(path, template_values))

	def SpecializationAlreadyExists(self, name):
		try:
			check = db.GqlQuery("SELECT * FROM Specialization WHERE specialization = :1", name)
		except:
			return False

		if check.get() is None:
			return False
		else:
			return True

