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
		do_commit = False
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break
		if check == True:
			new_course = Course()
			for result in validator.results:
				if result['key'] == "comment_course_id":
					if not self.CourseAlreadyExists(result['value']):
						new_course.course_id = result['value']
						do_commit = True
					else:
						result['valid'] = False
				elif result['key'] == "comment_course_name":
					new_course.course_name = result['value']

			if do_commit == True:
				new_course.put()

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

	def CourseAlreadyExists(self, name):
		try:
			check = db.GqlQuery("SELECT * FROM Course WHERE course_id = :1", name)
		except:
			return False

		if check.get() is None:
			return False
		else:
			return True

