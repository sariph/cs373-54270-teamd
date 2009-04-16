import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminMatch(webapp.RequestHandler):
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
		self.results = []
		self.finished = None
		self.match = None

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
			'finished': self.finished
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminMatch.html')
		self.response.out.write(template.render(path, template_values))

