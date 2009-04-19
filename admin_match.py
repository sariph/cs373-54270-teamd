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
		self.applicants = {}
		self.classes = {}
		'''
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.course_classes = None
		self.selected_course = None
		self.selected_class = None
		self.results = []
		self.finished = None
		self.match = None
		'''

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		applicants = db.GqlQuery("SELECT * FROM Applicant")
		classes = db.GqlQuery("SELECT * FROM Class")
		for applicant in applicants:
			user = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", applicant.UTEID).get()
#			applicant.__dict__.update(user.__dict__)
			applicant.first_name = user.first_name
			applicant.last_name = user.last_name
#			applicant.free = True
			applicant.points = {}
			for lcv in classes:
				applicant.points[lcv.key()] = 0
				if(applicant.specialization_comment == lcv.specialization_comment):
					applicant.points[lcv.key()] += 1
				elif(applicant.qualified_comment == lcv.course_id):
					applicant.points[lcv.key()] += 1
			self.applicants[applicant.key()] = applicant
		self.response.out.write(self.applicants)
		self.response.out.write("<br />\n")
		for lcv in classes:
			lcv.assigned = []
			lcv.free = True
			lcv.points = {}
			for applicant in applicants:
				lcv.points[applicant.key()] = 0
				if(lcv.native_english == "yes" and applicant.native_english == "no"):
					lcv.points[applicant.key()] -= 10
				elif(lcv.unwanted_comment == applicant.UTEID):
					lcv.points[applicant.key()] -= 100
				elif(lcv.wanted_comment == applicant.UTEID):
					lcv.points[applicant.key()] += 100
				elif(lcv.specialization_comment == applicant.specialization_comment):
					lcv.points[applicant.key()] += 1
			self.classes[lcv.key()] = lcv
		self.response.out.write(self.classes)
		self.response.out.write("<br />\n")
		result = self.SMP(self.applicants, self.classes)
		'''
		self.applicants = [i for i in db.GqlQuery("SELECT * FROM Course")]
		for lcv in self.applicants:
			self.response.out.write(lcv.to_xml())
		'''
		self.template()

	def SMP(self, applicants_with_points, classes_with_points):
		result = {}
		for key, applicant in applicants_with_points.items():
			# order tuples (class key, class points) by highest class points
			for highest_key_points in sorted(applicant.points.items(), self.sortfunc):
				# if highest class is free
				if(classes_with_points[highest_key_points[0]].free):
					# assign class to applicant and set free to False
					applicant.assigned = highest_key_points[0]
					applicant.free = False
					# assign applicant to class and set free to False if enough TAs
					classes_with_points[highest_key_points[0]].assigned.append(key)
					if(len(classes_with_points[highest_key_points[0]].assigned) == classes_with_points[highest_key_points[0]].numTA_needed):
						classes_with_points[highest_key_points[0]].free = False
					self.response.out.write("Assigning " + applicant.first_name + ' ' + applicant.last_name + " to " + classes_with_points[highest_key_points[0]].class_id)
					break
				# highest class is not free
				else:
					# check if current applicant is better match than any of the existing applicant(s)
					for existing_applicant_key in classes_with_points[highest_key_points[0]].assigned:
						if(classes_with_points[highest_key_points[0]].points[key] > classes_with_points[highest_key_points[0]].points[existing_applicant_key]):
# TODO swap them
							self.response.out.write("We found a replacement!")
							break
						# this else is for debugging, remove it
						else:
							self.response.out.write("We found no replacement")
		return result

	def sortfunc(self, x, y):
		return cmp(x[1], y[1])

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""

		'''
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

		# what is this?
		if result['valid'] == False:
			self.finished = None
		'''

		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'applicants': self.applicants,
			'classes': self.classes
		}
		'''
		template_values = {
			'results': self.results,
			'courses': self.courses,
			'course_classes': self.course_classes,
			'selected_course': self.selected_course,
			'selected_class': self.selected_class,
			'finished': self.finished
		}
		'''
		path = os.path.join(os.path.dirname(__file__), 'templates', 'adminMatch.html')
		self.response.out.write(template.render(path, template_values))

