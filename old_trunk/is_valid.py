import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class Is_valid(webapp.RequestHandler):
	"""
	Validates each field entry upon get request.
	"""
	def get(self):
		key = self.request.get('key')
		value = self.request.get('value')
		validator = Validator([(key, value)])
		self.response.headers['Content-Type'] = 'text/xml'
		self.response.out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
		self.response.out.write("<fields>\n")
		self.response.out.write("\t<field key=\"" + key + '" value="' + value + '" valid="' +  str(validator.results[0]['valid']) + "\" />\n")
		self.response.out.write("</fields>\n")

