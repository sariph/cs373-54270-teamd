import os
import Validation
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
	def get(self):
		"""
		Displays the class template.
		"""
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, {}))

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
				elif result['key'] == "comment_admission":
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

class InstructorMain(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def get(self):
		"""
		Displays the class template.
		"""
		path = os.path.join(os.path.dirname(__file__), 'instructor.html')
		self.response.out.write(template.render(path, {}))

class InstructorEdit(webapp.RequestHandler):
	"""
	Class for handling the instructor form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
		self.instructors = [i for i in db.GqlQuery("SELECT * FROM Instructor")]
		self.specializations = [i for i in db.GqlQuery("SELECT * FROM Specialization")]
		self.applicants = [i for i in db.GqlQuery("SELECT * FROM Applicant")]
		for applicant in self.applicants:
			applicant.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", applicant.UTEID).get()

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
			new_unwanted_student = Unwanted_Student()
			new_wanted_student = Wanted_Student()
			
			for result in validator.results:
				if result['key'] == "comment_wanted":
					new_wanted_student.UTEID = result['value']
					#new_wanted_student.class_id = 
				elif result['key'] == "comment_major":
					new_applicant.qualified_comment = result['value']
			new_wanted_student.put()

			
			
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'specializations' : self.specializations,
			'applicants' : self.applicants,
			'instructors' : self.instructors
		}
		path = os.path.join(os.path.dirname(__file__), 'instructorEdit.html')
		self.response.out.write(template.render(path, template_values))
		
class InstructorApp(webapp.RequestHandler):
	"""
	Class for handling the instructor form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = []
		self.instructors = [i for i in db.GqlQuery("SELECT * FROM User WHERE position = 'Professor'")]
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]

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
			new_instructor_app = Instructor_App()
			
			for result in validator.results:
				if result['key'] == "comment_uteid":
					new_instructor_app.UTEID = result['value']
				elif result['key'] == "comment_course_id":
					new_instructor_app.course_id = result['value']
			new_instructor_app.put()
			
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'instructors' : self.instructors,
			'courses' : self.courses
		}
		path = os.path.join(os.path.dirname(__file__), 'instructorapp.html')
		self.response.out.write(template.render(path, template_values))

class AdminMain(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
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
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
		}
		path = os.path.join(os.path.dirname(__file__), 'admin.html')
		self.response.out.write(template.render(path, template_values))
		
class AdminAddUsers(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
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
			new_user = User()
			for result in validator.results:
				if result['key'] == "comment_UTEID":
					new_user.UTEID = result['value']
				elif result['key'] == "comment_first_name":
					new_user.first_name = result['value']
				elif result['key'] == "comment_middle_name":
					new_user.middle_name = result['value']
				elif result['key'] == "comment_last_name":
					new_user.last_name = result['value']
				elif result['key'] == "comment_password":
					new_user.password= result['value']
				elif result['key'] == "phone_user":
					new_user.phone = db.PhoneNumber(result['value'])
				elif result['key'] == "email_user":
					new_user.email = db.Email(result['value'])
				elif result['key'] == "radio_position":
					new_user.position = result['value']
					
			if not self.UTEIDAlreadyExists(new_user.UTEID):
				new_user.put()
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
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddUsers.html')
		self.response.out.write(template.render(path, template_values))
		
	def UTEIDAlreadyExists(self, name):
		try:		
			check = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", name)
		except:
			return False
		
		if check.get() is None:
			return False
		else:
			return True
		
class AdminViewUsers(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.users = [i for i in db.GqlQuery("SELECT * FROM User")]

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
			'users': self.users,
		}
		path = os.path.join(os.path.dirname(__file__), 'adminViewUsers.html')
		self.response.out.write(template.render(path, template_values))
		
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
		
class AdminAddCourses(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
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
		do_commit = False
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break
		if check == True:
			new_course = Course()
			for result in validator.results:
				if result['key'] == "comment_course_id":
					if not self.CourseAlreadyExists(result['value']):
						new_course.course_id = result['value']
						do_commit = True
					else:
						result['valid'] = False
				elif result['key'] == "comment_course_name":
					new_course.course_name = result['value']

			if do_commit == True:
				new_course.put()
				
		self.results.extend(validator.results)
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'courses': [i for i in db.GqlQuery("SELECT * FROM Course")],
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddCourses.html')
		self.response.out.write(template.render(path, template_values))

	def CourseAlreadyExists(self, name):
		try:		
			check = db.GqlQuery("SELECT * FROM Course WHERE course_id = :1", name)
		except:
			return False
		
		if check.get() is None:
			return False
		else:
			return True

class AdminAddLanguages(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
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
			for result in validator.results:
				if not self.LanguageAlreadyExists(result['value']):
						language = Programming_Language(language=result['value'])
						language.put()
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
			'languages': [i for i in db.GqlQuery("SELECT * FROM Programming_Language")],
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddLanguages.html')
		self.response.out.write(template.render(path, template_values))

	def LanguageAlreadyExists(self, name):
		try:		
			check = db.GqlQuery("SELECT * FROM Programming_Language WHERE language = :1", name)
		except:
			return False
		
		if check.get() is None:
			return False
		else:
			return True

class AdminAddSpecializations(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
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
			for result in validator.results:
				if not self.SpecializationAlreadyExists(result['value']):
						specialization = Specialization(specialization=result['value'])
						specialization.put()
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
			'specializations': [i for i in db.GqlQuery("SELECT * FROM Specialization")],
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddSpecializations.html')
		self.response.out.write(template.render(path, template_values))

	def SpecializationAlreadyExists(self, name):
		try:		
			check = db.GqlQuery("SELECT * FROM Specialization WHERE specialization = :1", name)
		except:
			return False
		
		if check.get() is None:
			return False
		else:
			return True
		

class AdminAddMajors(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
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
			for result in validator.results:
				if not self.MajorAlreadyExists(result['value']):
						major = Major(major=result['value'])
						major.put()
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
			'majors': [i for i in db.GqlQuery("SELECT * FROM Major")],
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddMajors.html')
		self.response.out.write(template.render(path, template_values))

	def MajorAlreadyExists(self, name):
		try:		
			check = db.GqlQuery("SELECT * FROM Major WHERE major = :1", name)
		except:
			return False
		
		if check.get() is None:
			return False
		else:
			return True		

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
		path = os.path.join(os.path.dirname(__file__), 'adminAddClasses.html')
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
	
	
class AdminViewClasses(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.selected_course = None
		self.selected_class = None
		self.course_classes = []
		self.finished = None

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
		form_data = self.request.params.items()
		for field, option in form_data:
			if field == "select_course":
				self.selected_course = option
				self.course_classes = [i for i in db.GqlQuery("SELECT * FROM Class WHERE course_id = :1", option)]
			elif field == "select_class":
				self.selected_class = db.GqlQuery("SELECT * FROM Class WHERE class_id = :1", option).get()
				self.selected_class.instructor_info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", self.selected_class.instructor).get()
				TAs = [i for i in db.GqlQuery("SELECT * FROM TA WHERE class_id = :1", self.selected_class.class_id)]
				for ta in TAs:
					ta.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", ta.UTEID).get()
					
				self.selected_class.wanted_students = [db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", i.UTEID) for i in db.GqlQuery("SELECT * FROM Wanted_Student WHERE class_id = :1", self.selected_class.class_id)]
				
				self.selected_class.unwanted_students = [db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", i.UTEID) for i in db.GqlQuery("SELECT * FROM Unwanted_Student WHERE class_id = :1", self.selected_class.class_id)]
				self.finished = True
		
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'courses': self.courses,
			'selected_course': self.selected_course,
			'selected_class': self.selected_class,
			'course_classes': self.course_classes,
			'finished': self.finished,
		}
		path = os.path.join(os.path.dirname(__file__), 'adminViewClasses.html')
		self.response.out.write(template.render(path, template_values))
	
class AdminEditClasses(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.course_classes = None
		self.selected_course = None
		self.selected_class = None
		self.selected_option = None
		self.finished = None
		self.submitted_number = None
		self.applicants = []
		self.instructors = []
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
			elif field == "select_option":
				self.selected_option = option
				if option == "assign_instructor":
					self.instructors = [i for i in db.GqlQuery("SELECT * FROM Instructor_App WHERE course_id = :1",  self.selected_course)]
					for i in self.instructors:
						i.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", i.UTEID).get()
				elif option == "assign_ta":
					self.applicants = [i for i in db.GqlQuery("SELECT * FROM Applicant")]
					for app in self.applicants:
						app.info = db.GqlQuery("SELECT * FROM User WHERE UTEID = :1", app.UTEID).get()
				#elif option == "change_enrollment":
				#elif option == "change_num_ta":
			elif field == "instructor":
				self.selected_class.instructor = option
				self.selected_class.put()
				new_instructor = Instructor(UTEID = option, class_id = self.selected_class.class_id)
				new_instructor.put()
			elif field == "applicant":
				new_TA = TA(UTEID = option, class_id = self.selected_class.class_id)
				new_TA.put()
			elif field == "number_exp_enrollment":
				result['key'] = field
				result['value'] = option
				result['valid'] = Validation.number(option)
				self.results.append(result)
				if result['valid']:
					self.selected_class.expected_enrollment = int(option)
					self.selected_class.put()
					self.submitted_number = option
			elif field == "number_num_ta_needed":
				result['key'] = field
				result['value'] = option
				result['valid'] = Validation.number(option)
				self.results.append(result)
				if result['valid']:
					self.selected_class.numTA_needed = int(option)
					self.selected_class.put()
					self.submitted_number = option
			elif field == "finished":
				self.finished = option
		
		if result['valid'] == False:
			self.finished = None
		
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'courses': self.courses,
			'course_classes': self.course_classes,
			'selected_course': self.selected_course,
			'selected_class': self.selected_class,
			'selected_option': self.selected_option,
			'submitted_number': self.submitted_number,
			'instructors': self.instructors,
			'applicants': self.applicants,
			'finished': self.finished
		}
		path = os.path.join(os.path.dirname(__file__), 'adminEditClasses.html')
		self.response.out.write(template.render(path, template_values))

class AdminMatch(webapp.RequestHandler):
	"""
	Class for handling the admin form and validation.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.courses = [i for i in db.GqlQuery("SELECT * FROM Course")]
		self.course_classes = None
		self.selected_course = None
		self.selected_class = None
		self.results = []
		self.finished = None
		self.match = None

	def get(self):
		"""
		Displays the class template upon get request.
		"""
		self.template()

	def post(self):
		"""
		Validates form elements and will eventually submit the information to a database.
		"""
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
		
		if result['valid'] == False:
			self.finished = None
		
		self.template()

	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results': self.results,
			'courses': self.courses,
			'course_classes': self.course_classes,
			'selected_course': self.selected_course,
			'selected_class': self.selected_class,
			'finished': self.finished
		}
		path = os.path.join(os.path.dirname(__file__), 'adminMatch.html')
		self.response.out.write(template.render(path, template_values))

class TestDataModel(webapp.RequestHandler):
	"""
	Default class if nothing is passed to the index.
	"""
	def __init__(self):
		"""
		Constructor initializes results.
		"""
		self.results = ["START",""]
	def get(self):
		"""
		Displays the class template.
		"""
		#self.results.append("aaa")
		t = Test()
		t.start()
		#t.start()
		self.results.append(t.results)
		self.template()
	def template(self):
		"""
		Renders the template.
		"""
		template_values = {
			'results' : self.results
		}
		path = os.path.join(os.path.dirname(__file__), 'testdatamodel.html')
		self.response.out.write(template.render(path, template_values))

class Is_valid(webapp.RequestHandler):
	"""
	Validates each field entry upon get request.
	"""
	def get(self):
		key = self.request.get('key')
		value = self.request.get('value')
		validator = Validator([(key, value)])
		self.response.headers['Content-Type'] = 'text/xml'
		self.response.out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
		self.response.out.write("<fields>\n")
		self.response.out.write("\t<field key=\"" + key + '" value="' + value + '" valid="' +  str(validator.results[0]['valid']) + "\" />\n")
		self.response.out.write("</fields>\n")

application = webapp.WSGIApplication([('/is_valid', Is_valid),
                                      ('/applicant', TAApplicant),
				      ('/instructor', InstructorMain),
                                      ('/instructoredit', InstructorEdit),
				      ('/instructorapp', InstructorApp),
                                      ('/admin', AdminMain),
				      ('/adminaddusers', AdminAddUsers),
				      ('/adminviewusers', AdminViewUsers),
				      ('/adminviewapplicants', AdminViewApplicants),
				      ('/adminaddcourses', AdminAddCourses),
				      ('/adminaddmajors', AdminAddMajors),
				      ('/adminaddlanguages', AdminAddLanguages),
				      ('/adminaddspecializations', AdminAddSpecializations),
				      ('/adminaddclasses', AdminAddClasses),
				      ('/adminviewclasses', AdminViewClasses),
				      ('/admineditclasses', AdminEditClasses),
				      ('/adminmatch', AdminMatch),
				      ('/testdatamodel',TestDataModel),
                                      ('/.*', Index)])

def main():
	"""
	Runs the program when called.
	"""
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
