import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class TestDataModel(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = ["START",""]
	def get(self):
		"""
		Displays the class template.
		"""
		#self.results.append("aaa")
		t = Test()
		t.start()
		#t.start()
		self.results.append(t.results)
		self.template()
	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results' : self.results
		}
		#path = os.path.join(os.path.dirname(__file__), 'testdatamodel.html')
		#self.response.out.write(template.render(path, template_values))

