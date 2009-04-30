import os
import data_models
import data_utilities
import itertools

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminSearch(webapp.RequestHandler):
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

	def get(self):
		for iter in self.gen_or([data_models.Applicants, data_models.Instructors], ['first_name', 'last_name'], ['Steven', 'Baggs', 'Downing', 'Young']):
			for result in iter:
				self.response.out.write(result.first_name + ' ' + result.last_name)
				self.response.out.write('!\n')

		self.template()

	def gen_or(self, classes, fields, items):
		return itertools.chain((klass.all().filter('%s = ' % field, item) for klass in classes for field in fields for item in items))

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminSearch.html')
		self.response.out.write(template.render(path, template_values))

