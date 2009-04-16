import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class TAApplicant(webapp.RequestHandler):
	"""
	Class for handling the applicant form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
		self.eids = [i for i in db.GqlQuery("SELECT * FROM User WHERE position = 'Graduate'")]
		self.specializations = [i for i in db.GqlQuery("SELECT * FROM Specialization")]
		self.professors = [i for i in db.GqlQuery("SELECT * FROM User WHERE position = 'Professor'")]
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.majors = [i for i in db.GqlQuery("SELECT * FROM Major")]
		self.programming_languages = [i for i in db.GqlQuery("SELECT * FROM Programming_Language")]
		self.sel_languages = []
		self.sel_history = []
		self.sel_specializations = []
		self.sel_qualified = []

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		self.sel_languages = []
		self.sel_history = []
		self.sel_specializations = []
		self.sel_qualified = []
		validator = Validator(self.request.params.items())
		check = True
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break

		for result in validator.results:
			if result['value'] == 'language':
				self.sel_languages.append(result['key'])
			elif result['value'] == 'history':
				self.sel_history.append(result['key'])
			elif result['value'] == 'specialization':
				self.sel_specializations.append(result['key'])
			elif result['value'] == 'qualified':
				self.sel_qualified.append(result['key'])

		if check == True:
			new_applicant = Applicant()
			for result in validator.results:
				if result['key'] == "uniqueUTEID_UTEID":
					App_UTEID = result['value']
					new_applicant.UTEID = result['value']
				elif result['key'] == "comment_major":
					new_applicant.major = result['value']
				elif result['key'] == "date_admission":
					new_applicant.admission = result['value']
				elif result['key'] == "radio_phd":
					new_applicant.degree = result['value']
				elif result['key'] == "comment_supervising":
					new_applicant.supervisor = result['value']
				elif result['key'] == "radio_citizen":
					new_applicant.citizenship = result['value']
				elif result['key'] == "radio_native":
					new_applicant.native_english = result['value']
				elif result['key'] == "optional_ta":
					new_applicant.history_comment = result['value']
				elif result['key'] == "optional_programming":
					new_applicant.programming_comment = result['value']
				elif result['key'] == "optional_area":
					new_applicant.specialization_comment = result['value']
				elif result['key'] == "optional_qualified":
					new_applicant.qualified_comment = result['value']

			new_applicant.put()
			for sel in self.sel_languages:
				new_app_language = App_Programming_Language(UTEID=App_UTEID, language = sel)
				new_app_language.put()

			for sel in self.sel_history:
				new_course_history = App_History(UTEID=App_UTEID, course_id = sel)
				new_course_history.put()

			for sel in self.sel_specializations:
				new_specialization = App_Specialization(UTEID=App_UTEID, specialization = sel)
				new_specialization.put()

			for sel in self.sel_qualified:
				new_qualified_course = App_Qualified_Course(UTEID=App_UTEID, course_id = sel)
				new_qualified_course.put()


		self.results.extend(validator.results)
		self.template()


	def UTEIDAlreadyExists(self, name):
		try:
			check = db.GqlQuery("SELECT * FROM Applicant WHERE UTEID = :1", name)
		except:
			return False

		if check.get() is None:
			return False
		else:
			return True

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
                        'specializations' : self.specializations,
			'professors' : self.professors,
			'courses' : self.courses,
			'eids' : self.eids,
			'majors' : self.majors,
			'programming_languages' : self.programming_languages,
			'sel_languages': self.sel_languages,
			'sel_history': self.sel_history,
			'sel_specializations': self.sel_specializations,
			'sel_qualified': self.sel_qualified,
		}
		path = os.path.join(os.path.dirname(__file__), 'applicant.html')
		self.response.out.write(template.render(path, template_values))

