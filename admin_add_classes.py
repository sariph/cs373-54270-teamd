import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminAddClasses(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.course_ids = [i for i in db.GqlQuery("SELECT * FROM Course")]
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
			new_class = Class()
			for result in validator.results:
				if result['key'] == "comment_course_id":
					new_class.course_id = result['value']
				elif result['key'] == "unique_id":
					unique = result['value']
					new_class.unique_id = int(result['value'])
				elif result['key'] == "radio_class_semester":
					semester = result['value']
					new_class.semester = result['value']
				elif result['key'] == "radio_class_year":
					year = result['value']
					new_class.year = int(result['value'])
				elif result['key'] == "number_exp_enrollment":
					new_class.expected_enrollment = int(result['value'])
				elif result['key'] == "number_num_ta_needed":
					new_class.numTA_needed = int(result['value'])

			new_class.class_id = unique + semester + year

			if not self.ClassAlreadyExists(new_class.class_id):
				new_class.put()
			else:
				result['valid'] = False

		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'course_ids': self.course_ids,
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminAddClasses.html')
		self.response.out.write(template.render(path, template_values))

	def ClassAlreadyExists(self, name):
		try:
			check = db.GqlQuery("SELECT * FROM Class WHERE class_id = :1", name)
		except:
			return False

		if check.get() is None:
			return False
		else:
			return True

