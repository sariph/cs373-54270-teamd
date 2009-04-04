import os
import Debug
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
		self.results.extend(validator.results)
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
					new_user.phone = result['value']
				elif result['key'] == "email_user":
					new_user.email = result['value']
				elif result['key'] == "radio_position":
					new_user.position = result['value']
			new_user.put()
					
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
		for result in validator.results:
			if result['valid'] == False:
				check = False
				break
		if check == True:
			for result in validator.results:
				if not self.CourseAlreadyExists(result['value']):
						course = Course_Name(course_name=result['value'])
						course.put()
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
			'course_names': [i for i in db.GqlQuery("SELECT * FROM Course_Name")],
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddCourses.html')
		self.response.out.write(template.render(path, template_values))

	def CourseAlreadyExists(self, name):
		try:		
			check = db.GqlQuery("SELECT * FROM Course_Name WHERE course_name = :1", name)
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
		self.course_names = [i for i in db.GqlQuery("SELECT * FROM Course_Name")]
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
			'course_names': self.course_names,
		}
		path = os.path.join(os.path.dirname(__file__), 'adminAddClasses.html')
		self.response.out.write(template.render(path, template_values))
		
class AdminEditClasses(webapp.RequestHandler):
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
				      ('/adminaddcourses', AdminAddCourses),
				      ('/adminaddmajors', AdminAddMajors),
				      ('/adminaddlanguages', AdminAddLanguages),
				      ('/adminaddspecializations', AdminAddSpecializations),
				      ('/adminaddclasses', AdminAddClasses),
				      ('/admineditclasses', AdminEditClasses),
                                      ('/.*', Index)],
                                     debug=True)

def main():
	"""
	Runs the program when called.
	"""
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
