import os
import data_utilities

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminEmpty(webapp.RequestHandler):
	def get(self):
		system = data_utilities.initialize()
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminEmpty.html')
		self.response.out.write(template.render(path, template_values))

