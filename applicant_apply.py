import os
import data_models
import data_utilities

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class ApplicantApply(webapp.RequestHandler):
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Applicants' else False

		if(self.logged_in):
			data_utilities.insert_application(
				system.current_user,
				system.current_semester,
				None)

	def get(self):
#		system = data_utilities.initialize()
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'applicantApply.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

