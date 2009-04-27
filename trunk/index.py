import os
import Validation
import ta_applicant
import instructor_main
import instructor_edit
import instructor_app
import admin_main
import admin_add_users
import admin_view_users
import admin_view_applicants
import admin_add_courses
import admin_add_languages
import admin_add_specializations
import admin_add_majors
import admin_add_classes
import admin_view_classes
import admin_edit_classes
import admin_match
import test_data_model
import is_valid
import admin_change_phase

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class Index(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
	
	def get(self):
		"""
		Displays the class template.
		"""
		self.template()
		
	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
                    'results' : self.results,
                    'phase': [i for i in db.GqlQuery("SELECT * FROM Phase")]
		}
                path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([('/is_valid', is_valid.Is_valid),
                                      ('/applicant', ta_applicant.TAApplicant),
                                      ('/instructor', instructor_main.InstructorMain),
                                      ('/instructoredit', instructor_edit.InstructorEdit),
                                      ('/instructorapp', instructor_app.InstructorApp),
                                      ('/admin', admin_main.AdminMain),
                                      ('/adminaddusers', admin_add_users.AdminAddUsers),
                                      ('/adminviewusers', admin_view_users.AdminViewUsers),
#doesn't have template
                                      ('/adminviewapplicants', admin_view_applicants.AdminViewApplicants),
                                      ('/adminaddcourses', admin_add_courses.AdminAddCourses),
                                      ('/adminaddlanguages', admin_add_languages.AdminAddLanguages),
                                      ('/adminaddspecializations', admin_add_specializations.AdminAddSpecializations),
                                      ('/adminaddmajors', admin_add_majors.AdminAddMajors),
                                      ('/adminaddclasses', admin_add_classes.AdminAddClasses),
                                      ('/adminviewclasses', admin_view_classes.AdminViewClasses),
                                      ('/admineditclasses', admin_edit_classes.AdminEditClasses),
                                      ('/adminmatch', admin_match.AdminMatch),
                                      ('/testdatamodel', test_data_model.TestDataModel),
                                      ('/adminchangephase',admin_change_phase.AdminChangePhase),
                                      ('/.*', Index)])

def main():
	"""
	Runs the program when called.
	"""
	run_wsgi_app(application)
	

if __name__ == "__main__":
	main()

