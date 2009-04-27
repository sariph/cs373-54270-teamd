import os
import data_models
import data_utilities

from validator import Validator

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminInstructors(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.results = []
		self.instructors = [instructor for instructor in data_models.Instructors.all()]

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		if(all(map(self.check_valid, self.results))):
			data_utilities.insert_instructor(self.request.get('comment|ut_eid'), self.request.get('password|password'), self.request.get('comment|first_name'), self.request.get('comment|last_name'))
			self.instructors = [instructor for instructor in data_models.Instructors.all()]

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'instructors': self.instructors
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminInstructors.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

