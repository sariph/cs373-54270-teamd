import os
import data_models
import data_utilities

from validator import Validator

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminMatch(webapp.RequestHandler):
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.applicants = [application.applicant for application in data_models.Applications.gql('WHERE semester = :1', system.current_semester)]
		self.classes = [class_in_question for class_in_question in data_models.Classes.gql('WHERE semester = :1', system.current_semester)]
		self.matches = []
		self.results = []

	def get(self):
		self.matches = self.smp(self.rate())

		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		if(all(map(self.check_valid, self.results))):
			pass

		self.template()

	def rate(self):
		applicants_with_pref = []

		for applicant in self.applicants:
#			applicant.assigned = None
			applicant.pref = []
			for class_in_question in self.classes:
				points = 0
				points += self.points_specialization(applicant, class_in_question)
				points += self.points_qualified(applicant, class_in_question)
				applicant.pref.append((class_in_question, points))
			applicant.pref.sort(self.sortfunc)
			applicants_with_pref.append(applicant)

		for class_in_question in self.classes:
			class_in_question.assigned = []
			class_in_question.free = class_in_question.tas_needed
			class_in_question.pref = {}
			for applicant in self.applicants:
				points = 0
				points += self.points_specialization(applicant, class_in_question)
				points += self.points_qualified(applicant, class_in_question)
				points += self.points_native_english_speaker(applicant, class_in_question)
				points += self.points_wanted(applicant, class_in_question)
				points += self.points_unwanted(applicant, class_in_question)
				class_in_question.pref[applicant] = points
#			classes_with_pref[class_in_question] = pref
#			classes_with_pref[class_in_question.unique] = class_in_question
		return applicants_with_pref

	def points_specialization(self, applicant, class_in_question):
		return 1 if applicant.specialization and class_in_question.background and applicant.specialization.key() == class_in_question.background.key() else 0

	def points_qualified(self, applicant, class_in_question):
		return 1 if data_models.ApplicantsCourses.gql('WHERE applicant = :1 AND course = :2', applicant, class_in_question.course).get() else 0

	def points_native_english_speaker(self, applicant, class_in_question):
		return -10 if class_in_question.native_english_speaker and not applicant.native_english_speaker else 0

	def points_wanted(self, applicant, class_in_question):
		return 100 if data_models.ApplicantsWanted.gql('WHERE applicant = :1 AND class_in_question = :2', applicant, class_in_question).get() else 0

	def points_unwanted(self, applicant, class_in_question):
		return -100 if data_models.ApplicantsUnwanted.gql('WHERE applicant = :1 AND class_in_question = :2', applicant, class_in_question).get() else 0

	def smp(self, applicants_with_pref):
		while applicants_with_pref:
			applicant_with_pref = applicants_with_pref.pop()

			while applicant_with_pref.pref:
				class_in_question, point = applicant_with_pref.pref.pop()

				if class_in_question.free:
					self.response.out.write('assigning' + applicant_with_pref.first_name + ' ' + applicant_with_pref.last_name + '\n')
					class_in_question.assigned.append(applicant_with_pref)
					class_in_question.free -= 1
					break
				else:
					self.response.out.write('class already full, checking if ' + applicant_with_pref.first_name + ' is better\n')
					for existing_applicant in class_in_question.assigned:
						if class_in_question.pref[applicant_with_pref] > class_in_question.pref[existing_applicant]:
							class_in_question.assigned.remove(existing_applicant)
							class_in_question.assigned.append(applicant_with_pref)
							applicants_with_pref.append(existing_applicant)
							self.response.out.write('\treplacing ' + existing_applicant.first_name + ' with ' + applicant_with_pref.first_name + '\n')
							break
						else:
							self.response.out.write('\tcannot replace ' + existing_applicant.first_name + ' with ' + applicant_with_pref.first_name + '\n')
					break
			self.response.out.write('pop: ' + str(len(applicants_with_pref)) + '\n')
		return [(applicant, class_with_pref) for class_with_pref in self.classes for applicant in class_with_pref.assigned]
#		self.response.out.write([(applicant, applicant.assigned]) for applicant, pref in applicants_with_pref if applicant.assigned])
#		self.response.out.write([(applicant, applicant.assigned]) for applicant, pref in classes_with_pref if applicant.assigned])

	def sortfunc(self, x, y):
		return cmp(x[1], y[1]) # TODO I dunno if this is right order
#		return cmp(y[1], x[1]) # uncomment if wrong result

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'applicants': self.applicants,
			'classes': self.classes,
			'matches': self.matches
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminMatch.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

