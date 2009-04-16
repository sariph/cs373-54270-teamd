import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class InstructorApp(webapp.RequestHandler):
	"""
	Class for handling the instructor form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
		self.instructors = [i for i in db.GqlQuery("SELECT * FROM User WHERE position = 'Professor'")]
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]

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
		check = True
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break

		if check == True:
			new_instructor_app = Instructor_App()

			for result in validator.results:
				if result['key'] == "comment_uteid":
					new_instructor_app.UTEID = result['value']
				elif result['key'] == "comment_course_id":
					new_instructor_app.course_id = result['value']
			new_instructor_app.put()

		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'instructors' : self.instructors,
			'courses' : self.courses
		}
		path = os.path.join(os.path.dirname(__file__), 'instructorapp.html')
		self.response.out.write(template.render(path, template_values))

