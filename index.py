import os
import Validation
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

class Applicant(webapp.RequestHandler):
	"""
	Class for handling the applicant form and validation.
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
		path = os.path.join(os.path.dirname(__file__), 'applicant.html')
		self.response.out.write(template.render(path, template_values))

class Instructor(webapp.RequestHandler):
	"""
	Class for handling the instructor form and validation.
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
		path = os.path.join(os.path.dirname(__file__), 'instructor.html')
		self.response.out.write(template.render(path, template_values))

class Admin(webapp.RequestHandler):
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
		self.classes = [i for i in db.GqlQuery("SELECT * FROM Class")]
		for c in self.classes:
			c.course_name = db.GqlQuery("SELECT * FROM Course WHERE course_id =:1", c.course_id).get().course_name
			c.unwanted_students = [db.GqlQuery("SELECT * FROM Users WHERE UTEID =:1", i.UTEID) for i in db.GqlQuery("SELECT * FROM Unwanted_Student WHERE course_id =:1", c.class_id)]
			c.wanted_students = [db.GqlQuery("SELECT * FROM Users WHERE UTEID =:1", i.UTEID) for i in db.GqlQuery("SELECT * FROM Wanted_Student WHERE course_id =:1", c.class_id)]
			instructor = db.GqlQuery("SELECT * FROM User WHERE UTEID =:1", c.instructor).get()
			
			if instructor == None:
				c.instructor_name = None
			elif instructor.middle_name == None:
				c.instructor_name = instructor.first_name + " " + instructor.last_name
			else:
				c.instructor_name = instructor.first_name + " " + instructor.middle_name + " " + instructor.last_name 
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
			'classes': self.classes
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
			elif field == "instructor":
				self.selected_class.instructor = option
				self.selected_class.put()
				new_instructor = Instructor(UTEID = option, class_id = selected_class.class_id)
				new_instructor.put()
			elif field == "applicant":
				new_TA = TA(UTEID = option, class_id = selected_class.class_id)
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
			'finished': self.finished
		}
		path = os.path.join(os.path.dirname(__file__), 'adminEditClasses.html')
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
                                      ('/applicant', Applicant),
                                      ('/instructor', Instructor),
                                      ('/admin', Admin),
				      ('/adminaddusers', AdminAddUsers),
				      ('/adminviewusers', AdminViewUsers),
				      ('/adminaddcourses', AdminAddCourses),
				      ('/adminaddmajors', AdminAddMajors),
				      ('/adminaddlanguages', AdminAddLanguages),
				      ('/adminaddspecializations', AdminAddSpecializations),
				      ('/adminaddclasses', AdminAddClasses),
				      ('/adminviewclasses', AdminViewClasses),
				      ('/admineditclasses', AdminEditClasses),
                                      ('/.*', Index)])

def main():
	"""
	Runs the program when called.
	"""
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
