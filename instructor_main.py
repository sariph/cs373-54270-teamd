import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class InstructorMain(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def get(self):
		"""
		Displays the class template.
		"""
		path = os.path.join(os.path.dirname(__file__), 'instructor.html')
		self.response.out.write(template.render(path, {}))
