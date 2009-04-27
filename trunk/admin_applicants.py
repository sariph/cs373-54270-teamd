import os
import data_models
import data_utilities

from validator import Validator

from datetime import date
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminApplicants(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.results = []
		self.applicants = [applicant for applicant in data_models.Applicants.all()]
		self.majors = [major for major in data_models.Majors.all()]
		self.phd = 'True'
		self.supervising_professors = [supervising_professor for supervising_professor in data_models.Instructors.all()]
		self.citizen = 'True'
		self.native_english_speaker = 'True'
		self.programming_languages = [programming_language for programming_language in data_models.ProgrammingLanguages.all()]
		self.specializations = [specialization for specialization in data_models.Specializations.all()]
		self.courses = [course for course in data_models.Courses.all()]

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		self.phd = self.request.get('boolean|phd')
		self.citizen = self.request.get('boolean|citizen')
		self.native_english_speaker = self.request.get('boolean|native_english_speaker')

		if(all(map(self.check_valid, self.results))):
			applicant = data_utilities.insert_applicant(
				self.request.get('comment|ut_eid'),
				self.request.get('password|password'),
				self.request.get('comment|first_name'),
				self.request.get('comment|last_name'),
				db.PhoneNumber(self.request.get('phone|phone')),
				db.Email(self.request.get('email|email')),
				db.GqlQuery('SELECT * FROM Majors WHERE abbr = :1', self.request.get('select|major')).get(),
				date(int(self.request.get('date|admission').split('-')[0]), int(self.request.get('date|admission').split('-')[1]), int(self.request.get('date|admission').split('-')[2])),
				(self.request.get('boolean|phd') == 'True'),
				data_models.Instructors.gql('WHERE ut_eid = :1', self.request.get('select|supervising_professor')).get(),
				(self.request.get('boolean|citizen') == 'True'),
				(self.request.get('boolean|native_english_speaker') == 'True'),
				db.GqlQuery('SELECT * FROM Specializations WHERE name = :1', self.request.get('select|specialization')).get())

			for removal in data_models.ApplicantsProgrammingLanguages.gql('WHERE applicant = :1', applicant):
				removal.delete()
			for programming_language in self.request.get_all('select|programming_languages'):
				data_utilities.insert_applicant_programming_language(applicant, data_models.ProgrammingLanguages.gql('WHERE name = :1', programming_language).get())

			for removal in data_models.ApplicantsCourses.gql('WHERE applicant = :1', applicant):
				removal.delete()
			for course in self.request.get_all('select|courses'):
				data_utilities.insert_applicant_course(applicant, data_models.Courses.gql('WHERE number = :1', course).get())

			self.applicants = [applicant for applicant in data_models.Applicants.all()]
#			data_utilities.insert_instructor(self.request.get('comment|ut_eid'), self.request.get('password|password'), self.request.get('comment|first_name'), self.request.get('comment|last_name'))
#			self.instructors = [instructor for instructor in db.GqlQuery('SELECT * FROM Instructors')]

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'applicants': self.applicants,
			'majors': self.majors,
			'phd': self.phd,
			'supervising_professors': self.supervising_professors,
			'citizen': self.citizen,
			'native_english_speaker': self.native_english_speaker,
			'programming_languages': self.programming_languages,
			'specializations': self.specializations,
			'courses': self.courses
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminApplicants.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

