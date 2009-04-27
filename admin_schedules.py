import os
import data_models
import data_utilities

from validator import Validator

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class AdminSchedules(webapp.RequestHandler):
	def __init__(self):
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		self.logged_in = True if system.current_user and system.current_user.class_name() == 'Admin' else False

		self.results = []
		self.form = 'courses'
		self.courses = [course for course in db.GqlQuery('SELECT * FROM Courses')]
		self.majors = [major for major in db.GqlQuery('SELECT * FROM Majors')]
		self.course = ''
		self.classes = []
		self.instructors = [instructor for instructor in data_models.Instructors.all()]

#		self.season = system.current_semester.season.name
#		self.phase = system.current_semester.phase.name
#		self.year = system.current_semester.year.strftime('%Y')

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		if self.request.get('select|courses'):
			self.form = 'courses'

			if(all(map(self.check_valid, self.results))):
				data_utilities.insert_course(
					db.GqlQuery('SELECT * FROM Majors WHERE abbr = :1', self.request.get('select|major')).get(),
					self.request.get('comment|number'),
					self.request.get('comment|name'))
				self.courses = [course for course in db.GqlQuery('SELECT * FROM Courses')]
				#db.GqlQuery('SELECT * FROM Majors WHERE abbr = :1', self.request.get('select|major')).get(),
#				data_utilities.insert_major(self.request.get('abbr|abbr'), self.request.get('comment|name'))
#				self.majors = [major for major in db.GqlQuery('SELECT * FROM Majors')]
		elif self.request.get('select|class'):
			self.results = []
			self.form = 'classes'
			self.course = db.GqlQuery('SELECT * FROM Courses WHERE number = :1', self.request.get('select|class')).get()
			self.classes = [class_in_question for class_in_question in db.GqlQuery('SELECT * FROM Classes WHERE course = :1 AND semester = :2', self.course, data_models.System.all().get().current_semester)]
		elif self.request.get('select|classes'):
			self.form = 'classes'
			self.course = db.GqlQuery('SELECT * FROM Courses WHERE number = :1', self.request.get('comment|course')).get()
			self.classes = [class_in_question for class_in_question in db.GqlQuery('SELECT * FROM Classes WHERE course = :1 AND semester = :2', self.course, data_models.System.all().get().current_semester)]

			if(all(map(self.check_valid, self.results))):
				data_utilities.insert_class(
					self.course,
					data_models.System.all().get().current_semester,
					data_models.Instructors.gql('WHERE ut_eid = :1', self.request.get('select|instructor')).get(),
					int(self.request.get('unique|unique')),
					int(self.request.get('number|enrollment')),
					int(self.request.get('number|tas_needed')),
					None,
					None)
				self.classes = [class_in_question for class_in_question in db.GqlQuery('SELECT * FROM Classes WHERE course = :1 AND semester = :2', self.course, data_models.System.all().get().current_semester)]

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'form': self.form,
			'courses': self.courses,
			'majors': self.majors,
			'course': self.course,
			'classes': self.classes,
			'instructors': self.instructors
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminSchedules.html' if self.logged_in else 'index.html')
		self.response.out.write(template.render(path, template_values))

	def check_valid(self, dict):
		return True if dict['valid'] else False

