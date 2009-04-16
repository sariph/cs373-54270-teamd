import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminEditClasses(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.course_classes = None
		self.selected_course = None
		self.selected_class = None
		self.selected_option = None
		self.finished = None
		self.submitted_number = None
		self.applicants = []
		self.instructors = []
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
		form_data = self.request.params.items()
		result = {}
		result['valid'] = True
		self.finished = None
		for field, option in form_data:
			if field == "select_course":
				self.selected_course = option
				self.course_classes = [i for i in db.GqlQuery("SELECT * FROM Class WHERE course_id = :1", option)]
			elif field == "select_class":
				self.selected_class = db.GqlQuery("SELECT * FROM Class WHERE class_id = :1", option).get()
			elif field == "select_option":
				self.selected_option = option
				if option == "assign_instructor":
					self.instructors = [i for i in db.GqlQuery("SELECT * FROM Instructor_App WHERE course_id = :1",  self.selected_course)]
					for i in self.instructors:
						i.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", i.UTEID).get()
				elif option == "assign_ta":
					self.applicants = [i for i in db.GqlQuery("SELECT * FROM Applicant")]
					for app in self.applicants:
						app.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", app.UTEID).get()
				#elif option == "change_enrollment":
				#elif option == "change_num_ta":
			elif field == "instructor":
				self.selected_class.instructor = option
				self.selected_class.put()
				new_instructor = Instructor(UTEID = option, class_id = self.selected_class.class_id)
				new_instructor.put()
			elif field == "applicant":
				new_TA = TA(UTEID = option, class_id = self.selected_class.class_id)
				new_TA.put()
			elif field == "number_exp_enrollment":
				result['key'] = field
				result['value'] = option
				result['valid'] = Validation.number(option)
				self.results.append(result)
				if result['valid']:
					self.selected_class.expected_enrollment = int(option)
					self.selected_class.put()
					self.submitted_number = option
			elif field == "number_num_ta_needed":
				result['key'] = field
				result['value'] = option
				result['valid'] = Validation.number(option)
				self.results.append(result)
				if result['valid']:
					self.selected_class.numTA_needed = int(option)
					self.selected_class.put()
					self.submitted_number = option
			elif field == "finished":
				self.finished = option

		if result['valid'] == False:
			self.finished = None

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'courses': self.courses,
			'course_classes': self.course_classes,
			'selected_course': self.selected_course,
			'selected_class': self.selected_class,
			'selected_option': self.selected_option,
			'submitted_number': self.submitted_number,
			'instructors': self.instructors,
			'applicants': self.applicants,
			'finished': self.finished
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminEditClasses.html')
		self.response.out.write(template.render(path, template_values))

