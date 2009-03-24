import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class Applicant(webapp.RequestHandler):
	def __init__(self):
		self.results = []

	def get(self):
		self.template()

	def post(self):
		validator = Validator(self.request.params.items())
		self.results.extend(validator.results)
		self.template()

	def template(self):
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'applicant.html')
		self.response.out.write(template.render(path, template_values))

class Instructor(webapp.RequestHandler):
	def __init__(self):
		self.results = []

	def get(self):
		self.template()

	def post(self):
		validator = Validator(self.request.params.items())
		self.results.extend(validator.results)
		self.template()

	def template(self):
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'instructor.html')
		self.response.out.write(template.render(path, template_values))

class Admin(webapp.RequestHandler):
	def __init__(self):
		self.results = []

	def get(self):
		self.template()

	def post(self):
		validator = Validator(self.request.params.items())
		self.results.extend(validator.results)
		self.template()

	def template(self):
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, template_values))

class Is_valid(webapp.RequestHandler):
	def get(self):
		key = self.request.get('key')
		value = self.request.get('value')
		validator = Validator([(key, value)])
#		self.response.headers['Content-Type'] = 'text/html'
#		self.response.out.write('True' if validator.valid else 'False')
		self.response.headers['Content-Type'] = 'text/xml'
		self.response.out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
		self.response.out.write("<fields>\n")
		self.response.out.write("\t<field key=\"" + key + '" value="' + value + '" valid="' + str(validator.results[0]['valid']) + "\" />\n")
		self.response.out.write("</fields>\n")

application = webapp.WSGIApplication([('/is_valid', Is_valid),
                                      ('/applicant', Applicant),
                                      ('/instructor', Instructor),
                                      ('/admin', Admin)],
                                     debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()

