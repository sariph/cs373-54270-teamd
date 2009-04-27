import os

from validator import Validator
from google.appengine.ext import webapp

class IsValid(webapp.RequestHandler):
	"""
	Validates each field entry upon get request.
	"""
	def get(self):
		key = self.request.get('key')
		value = self.request.get('value')
		validator = Validator(dict([(key, value)]))
		self.response.headers['Content-Type'] = 'text/xml'
		self.response.out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
		self.response.out.write("<fields>\n")
		self.response.out.write("\t<field key=\"" + key + '" value="' + value + '" valid="' +  str(validator.results[0]['valid']) + "\" />\n")
		self.response.out.write("</fields>\n")

