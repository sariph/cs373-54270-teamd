import os
import data_models
import data_utilities

from validator import Validator

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminTime(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		global system
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.results = []
		self.season = system.current_semester.season.name
		self.phase = system.current_semester.phase.name
		self.year = system.current_semester.year.strftime('%Y')

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

#		self.seasons = self.request.get_all('select|season') # for multiple value selects
#		self.season = self.request.get('select|season')
		self.season = self.request.get('radio|season')
		self.phase = self.request.get('radio|phase')
		self.year = self.request.get('year|year')

		if(all(map(self.check_valid, self.results))):
			data_utilities.insert_system(data_utilities.insert_semester(data_utilities.insert_phase(self.phase), data_utilities.insert_season(self.season), self.year), system.current_user)

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
#			'seasons': self.seasons,
			'results': self.results,
			'season': self.season,
			'phase': self.phase,
			'year': self.year
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminTime.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

