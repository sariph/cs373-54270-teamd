import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminChangePhase(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.phase = db.GqlQuery("SELECT * FROM Phase")

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
		do_commit = False
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break
		if check == True:
			new_phase = Phase()
			for result in validator.results:
				if result['key'] == "comment_phase":
                                        new_phase.phase = result['value']
                                        new_phase.put()
                                        break

		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
                        'phase' : self.phase
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminChangePhase.html')
		self.response.out.write(template.render(path, template_values))


