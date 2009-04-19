import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminViewClasses(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.selected_course = None
		self.selected_class = None
		self.course_classes = []
		self.finished = None

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
		for field, option in form_data:
			if field == "select_course":
				self.selected_course = db.get(db.Key(option))
				self.course_classes = [i for i in db.GqlQuery("SELECT * FROM Class WHERE course_id = :1 AND course_name = :2", self.selected_course.course_id, self.selected_course.course_name)]
			elif field == "select_class":
				self.selected_class = db.GqlQuery("SELECT * FROM Class WHERE class_id = :1", option).get()
				self.selected_class.instructor_info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", self.selected_class.instructor).get()
				TAs = [i for i in db.GqlQuery("SELECT * FROM TA WHERE class_id = :1", self.selected_class.class_id)]
				for ta in TAs:
					ta.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", ta.UTEID).get()

				self.selected_class.wanted_students = [db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", i.UTEID) for i in db.GqlQuery("SELECT * FROM Wanted_Student WHERE class_id = :1", self.selected_class.class_id)]

				self.selected_class.unwanted_students = [db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", i.UTEID) for i in db.GqlQuery("SELECT * FROM Unwanted_Student WHERE class_id = :1", self.selected_class.class_id)]
				self.finished = True

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'courses': self.courses,
			'selected_course': self.selected_course,
			'selected_class': self.selected_class,
			'course_classes': self.course_classes,
			'finished': self.finished,
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminViewClasses.html')
		self.response.out.write(template.render(path, template_values))

