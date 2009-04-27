import os
import data_utilities

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminReset(webapp.RequestHandler):
	def get(self):
		data_utilities.load_test_data()
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminReset.html')
		self.response.out.write(template.render(path, template_values))

