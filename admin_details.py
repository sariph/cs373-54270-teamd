import os
import data_models
import data_utilities

from validator import Validator

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminDetails(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.results = []
		self.form = ''
		self.majors = [major for major in db.GqlQuery('SELECT * FROM Majors')]
		self.programming_languages = [programming_language for programming_language in db.GqlQuery('SELECT * FROM ProgrammingLanguages')]
		self.specializations = [specialization for specialization in db.GqlQuery('SELECT * FROM Specializations')]
#		self.season = system.current_semester.season.name
#		self.phase = system.current_semester.phase.name
#		self.year = system.current_semester.year.strftime('%Y')

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		if self.request.get('select|majors'):
			self.form = 'majors'

			if(all(map(self.check_valid, self.results))):
				data_utilities.insert_major(self.request.get('abbr|abbr'), self.request.get('comment|name'))
				self.majors = [major for major in db.GqlQuery('SELECT * FROM Majors')]
		elif self.request.get('select|programming_languages'):
			self.form = 'programming_languages'

			if(all(map(self.check_valid, self.results))):
				data_utilities.insert_programming_language(self.request.get('comment|programming_language'))
				self.programming_languages = [programming_language for programming_language in db.GqlQuery('SELECT * FROM ProgrammingLanguages')]
		elif self.request.get('select|specializations'):
			self.form = 'specializations'

			if(all(map(self.check_valid, self.results))):
				data_utilities.insert_specialization(self.request.get('comment|specialization'))
				self.specializations = [specialization for specialization in db.GqlQuery('SELECT * FROM Specializations')]

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'form': self.form,
			'majors': self.majors,
			'programming_languages': self.programming_languages,
			'specializations': self.specializations
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminDetails.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

