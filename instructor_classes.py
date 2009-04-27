import os
import data_models
import data_utilities

from validator import Validator

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class InstructorClasses(webapp.RequestHandler):
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Instructors' else False

		self.results = []
		self.form = 'classes'
		self.classes = [class_in_question for class_in_question in data_models.Classes.gql('WHERE semester = :1 AND instructor = :2', system.current_semester, system.current_user)]
		self.class_in_question = ''
		self.applicants = [application.applicant for application in data_models.Applications.gql('WHERE semester = :1', system.current_semester)]
		self.applicants_wanted = []
		self.applicants_unwanted = []
		self.native_english_speaker = 'True'
		self.specializations = [specialization for specialization in data_models.Specializations.all()]

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		if self.request.get('select|detail'):
			self.results = []
			self.form = 'details'
			self.class_in_question = data_models.Classes.gql('WHERE unique = :1', int(self.request.get('select|detail'))).get()
			self.applicants_wanted = [applicant_wanted for applicant_wanted in data_models.ApplicantsWanted.gql('WHERE class_in_question = :1', self.class_in_question)]
			self.applicants_unwanted = [applicant_unwanted for applicant_unwanted in data_models.ApplicantsUnwanted.gql('WHERE class_in_question = :1', self.class_in_question)]
		elif self.request.get('select|details'):
			self.form = 'details'
			self.class_in_question = data_models.Classes.gql('WHERE unique = :1', int(self.request.get('comment|class'))).get()
			self.applicants_wanted = [applicant_wanted for applicant_wanted in data_models.ApplicantsWanted.gql('WHERE class_in_question = :1', self.class_in_question)]
			self.applicants_unwanted = [applicant_unwanted for applicant_unwanted in data_models.ApplicantsUnwanted.gql('WHERE class_in_question = :1', self.class_in_question)]
			self.native_english_speaker = self.request.get('boolean|native_english_speaker')

			if(all(map(self.check_valid, self.results))):
				data_utilities.insert_class(
					self.class_in_question.course,
					self.class_in_question.semester,
					self.class_in_question.instructor,
					self.class_in_question.unique,
					self.class_in_question.enrollment,
					self.class_in_question.tas_needed,
					(self.native_english_speaker == 'True'),
					db.GqlQuery('SELECT * FROM Specializations WHERE name = :1', self.request.get('select|background')).get())

			for removal in data_models.ApplicantsWanted.gql('WHERE class_in_question = :1', self.class_in_question):
				removal.delete()
			for applicant in self.request.get_all('select|wanted'):
				data_utilities.insert_applicant_wanted(data_models.Applicants.gql('WHERE ut_eid = :1', applicant).get(), self.class_in_question)

			for removal in data_models.ApplicantsUnwanted.gql('WHERE class_in_question = :1', self.class_in_question):
				removal.delete()
			for applicant in self.request.get_all('select|unwanted'):
				data_utilities.insert_applicant_unwanted(data_models.Applicants.gql('WHERE ut_eid = :1', applicant).get(), self.class_in_question)

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'form': self.form,
			'classes': self.classes,
			'class_in_question': self.class_in_question,
			'applicants': self.applicants,
			'applicants_wanted': self.applicants_wanted,
			'applicants_unwanted': self.applicants_unwanted,
			'native_english_speaker': self.native_english_speaker,
			'specializations': self.specializations
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'instructorClasses.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

