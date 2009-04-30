import os
import data_models
import data_utilities
import itertools
import re

from validator import Validator

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminSearch(webapp.RequestHandler):
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.results = []
		self.search_results = []

	def get(self):
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		if(all(map(self.check_valid, self.results))):
			for result in self.or_query([data_models.Applicants, data_models.Instructors], ['ut_eid', 'first_name', 'last_name'], re.split('\W+', self.request.get('comment|search'))):
				if(isinstance(result, data_models.Applicants)):
					result.type = 'Applicants'
					self.search_results.append(result)
				elif(isinstance(result, data_models.Instructors)):
					result.type = 'Instructors'
					self.search_results.append(result)

		self.template()

	def or_query(self, classes, fields, items):
		"""
		Returns a list of Entities from any of the Models in the classes list, such that there exists a field from fields that matches an item from items
		"""
		return dict([(entity.key(), entity) for iter in itertools.chain((klass.all().filter('%s = ' % field, item) for klass in classes for field in fields for item in items)) for entity in iter]).values()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'search_results': self.search_results
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminSearch.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

