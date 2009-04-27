import os
import data_models
import data_utilities

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Admin(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.phase = system.current_semester.phase.name

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'phase': self.phase
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'admin.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

