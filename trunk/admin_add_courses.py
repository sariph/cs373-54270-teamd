import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminAddCourses(webapp.RequestHandler):
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
		check = True
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break
			
		if check == True:
			new_course_id = self.request.get("courseid")
			new_course_name = self.request.get("coursename")
			if db.GqlQuery("SELECT * FROM Course WHERE courseid = :1 AND coursename = :2",  new_course_id, new_course_name).get() is not None:
				new_course = Course(course_id = new_course_id, course_name = new_course_name)
				new_course.put
			else:
				for result in validator.results:
					result['valid'] = False

		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'courses': [i for i in db.GqlQuery("SELECT * FROM Course")],
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminAddCourses.html')
		self.response.out.write(template.render(path, template_values))
