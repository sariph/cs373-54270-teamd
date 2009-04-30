import os
import data_models
import data_utilities

from validator import Validator
from is_valid import IsValid
from admin import Admin
from admin_time import AdminTime
from admin_details import AdminDetails
from admin_instructors import AdminInstructors
from admin_applicants import AdminApplicants
from admin_schedules import AdminSchedules
from admin_match import AdminMatch
from admin_search import AdminSearch
from admin_empty import AdminEmpty
from admin_reset import AdminReset
from applicant import Applicant
from applicant_details import ApplicantDetails
from applicant_apply import ApplicantApply
from instructor import Instructor
from instructor_classes import InstructorClasses

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Index(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def __init__(self):
		global system
		system = data_models.System.all().get()
		if system is None:
			system = data_utilities.initialize()
		system.current_user = None
		system.put()

		self.results = []

	def get(self):
		"""
		Displays the class template.
		"""
		self.template()

	def post(self):
		"""
		Handles login
		"""
		validator = Validator(self.request.params)
		self.results.extend(validator.results)

		ut_eid = self.request.get('ut_eid|ut_eid')
		password = self.request.get('password|password')

		admin = data_models.Admin.gql('WHERE ut_eid = :1 AND password = :2', ut_eid, password).get()
		applicant = data_models.Applicants.gql('WHERE ut_eid = :1 AND password = :2', ut_eid, password).get()
		instructor = data_models.Instructors.gql('WHERE ut_eid = :1 AND password = :2', ut_eid, password).get()
		if admin:
			system.current_user = admin
			system.put()
			self.redirect('/admin')
		elif applicant:
			system.current_user = applicant
			system.put()
			self.redirect('/applicant')
		elif instructor:
			system.current_user = instructor
			system.put()
			self.redirect('/instructor')

		# validate and build template for error display
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results
		}
		path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/isValid', IsValid),
                                      ('/admin', Admin),
                                      ('/adminTime', AdminTime),
                                      ('/adminDetails', AdminDetails),
                                      ('/adminInstructors', AdminInstructors),
                                      ('/adminApplicants', AdminApplicants),
                                      ('/adminSchedules', AdminSchedules),
                                      ('/adminMatch', AdminMatch),
                                      ('/adminSearch', AdminSearch),
                                      ('/adminEmpty', AdminEmpty),
                                      ('/adminReset', AdminReset),
                                      ('/applicant', Applicant),
                                      ('/applicantDetails', ApplicantDetails),
                                      ('/applicantApply', ApplicantApply),
                                      ('/instructor', Instructor),
                                      ('/instructorClasses', InstructorClasses),
                                      ('/.*', Index)])

def main():
	"""
	Runs the program when called.
	"""
	run_wsgi_app(application)

if __name__ == "__main__":
	main()

