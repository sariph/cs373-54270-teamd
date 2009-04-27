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
			p = Phase.all()
			phase = p.fetch(1)
			db.delete(phase)
			for result in validator.results:
				if result['key'] == "radio_phase":
                                        phase = Phase()
                                        phase.phase = int(result['value'])
                                        db.put(phase)
                                        break
                                break
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
                    'results' : self.results,
                    'phase': [i for i in db.GqlQuery("SELECT * FROM Phase")]
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminChangePhase.html')
		self.response.out.write(template.render(path, template_values))


