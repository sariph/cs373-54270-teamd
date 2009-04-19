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
		self.show_error = False
		self.done = False
		self.classes = [i for i in db.GqlQuery("SELECT * FROM Class")]
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
		self.results = validator.results
		selected_class_id = self.request.get("comment_class")
		selected_class = db.GqlQuery("SELECT * FROM Class WHERE class_id = :1", selected_class_id).get()
		wanted = self.request.get("comment_wanted", allow_multiple=True)
		unwanted = self.request.get("comment_unwanted", allow_multiple=True)
		
		self.show_error = False
		
		for w in wanted:
			for u in unwanted:
				if u == w:
					self.show_error = True
		
		if self.show_error != True:
			for old_wanted in db.GqlQuery("SELECT * FROM Wanted_Student WHERE class_id = :1", selected_class_id):
				old_wanted.delete()
			
			for old_unwanted in db.GqlQuery("SELECT * FROM Unwanted_Student WHERE class_id = :1", selected_class_id):
				old_unwanted.delete()
			
			selected_class.native_english = self.request.get("radio_native")
			selected_class.put()
			for w in wanted:
				new_wanted = Wanted_Student(class_id = selected_class_id, UTEID = w)
				new_wanted.put()
				
			for u in unwanted:
				new_unwanted = Unwanted_Student(class_id = selected_class_id, UTEID = u)
				new_unwanted.put()
		
			Requested_Specialization(specialization = self.request.params["comment_specialization_drop"], class_id = selected_class_id).put()
		
			self.done = True
			
		
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
			'instructors' : self.instructors,
			'classes'	: self.classes,
			'error': self.show_error,
			'done': self.done
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'instructorEdit.html')
		self.response.out.write(template.render(path, template_values))

