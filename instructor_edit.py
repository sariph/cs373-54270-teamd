import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class InstructorEdit(webapp.RequestHandler):
	"""
	Class for handling the instructor form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
		self.instructors = [i for i in db.GqlQuery("SELECT * FROM Instructor")]
		self.specializations = [i for i in db.GqlQuery("SELECT * FROM Specialization")]
		self.applicants = [i for i in db.GqlQuery("SELECT * FROM Applicant")]
		for applicant in self.applicants:
			applicant.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", applicant.UTEID).get()

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
			new_unwanted_student = Unwanted_Student()
			new_wanted_student = Wanted_Student()

			for result in validator.results:
				if result['key'] == "comment_wanted":
					new_wanted_student.UTEID = result['value']
					#new_wanted_student.class_id =
				elif result['key'] == "comment_major":
					new_applicant.qualified_comment = result['value']
			new_wanted_student.put()

		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'specializations' : self.specializations,
			'applicants' : self.applicants,
			'instructors' : self.instructors
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'instructorEdit.html')
		self.response.out.write(template.render(path, template_values))

