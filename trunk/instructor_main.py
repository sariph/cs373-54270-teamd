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
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
	def get(self):
		"""
		Displays the class template.
		"""
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
                    'results' : self.results,
                    'phase': [i for i in db.GqlQuery("SELECT * FROM Phase")]
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'instructor.html')
		self.response.out.write(template.render(path, template_values))

