import os
import Validation

from TestDataModel import *
from DataModels import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from validator import Validator

class AdminViewApplicants(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.applicants = [i for i in db.GqlQuery("SELECT * FROM Applicant")]

		for app in self.applicants:
			app.user_info = db.GqlQuery("SELECT * FROM User WHERE UTEID=:1", app.UTEID).get()
			app.languages = [i for i in db.GqlQuery("SELECT * FROM App_Programming_Language WHERE UTEID=:1", app.UTEID)]
			app.history = [i for i in db.GqlQuery("SELECT * FROM App_History WHERE UTEID=:1", app.UTEID)]
			app.specializations = [i for i in db.GqlQuery("SELECT * FROM App_Specialization WHERE UTEID=:1", app.UTEID)]
			app.qualified_courses = [i for i in db.GqlQuery("SELECT * FROM App_Qualified_Course WHERE UTEID=:1", app.UTEID)]
			app.supervisor_info = db.GqlQuery("SELECT * FROM User WHERE UTEID=:1", app.supervisor).get()



	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'applicants': self.applicants,
		}
		path = os.path.join(os.path.dirname(__file__), 'adminViewApplicants.html')
		self.response.out.write(template.render(path, template_values))

