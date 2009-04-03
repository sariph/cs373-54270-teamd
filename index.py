import os
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class Index(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def get(self):
		"""
		Displays the class template.
		"""
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, {}))

class Applicant(webapp.RequestHandler):
	"""
	Class for handling the applicant form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		validator = Validator(self.request.params.items())
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'applicant.html')
		self.response.out.write(template.render(path, template_values))

class Instructor(webapp.RequestHandler):
	"""
	Class for handling the instructor form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		validator = Validator(self.request.params.items())
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'instructor.html')
		self.response.out.write(template.render(path, template_values))

class Admin(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		validator = Validator(self.request.params.items())
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, template_values))

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
		self.response.out.write("\t<field key=\"" + key + '" value="' + value + '" valid="' + str(validator.results[0]['valid']) + "\" />\n")
		self.response.out.write("</fields>\n")

application = webapp.WSGIApplication([('/is_valid', Is_valid),
                                      ('/applicant', Applicant),
                                      ('/instructor', Instructor),
                                      ('/admin', Admin),
                                      ('/.*', Index)],
                                     debug=True)

def main():
	"""
	Runs the program when called.
	"""
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
