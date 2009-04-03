import cgi

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class User(db.Model):
	UTEID = db.StringProperty()		#Primary key
	first_name = db.StringProperty()
	last_name = db.StringProperty()
	middle_name = db.StringProperty()
	password = db.StringProperty()
	phone = db.PhoneNumberProperty()
	email = db.EmailProperty()
	
#Subclasses of User. Using the Relational scheme from the DB book
class TA(db.Model):
	UTEID = db.StringProperty()	
	unique_id = db.IntegerProperty()	#unique_id the TA is assigned to
	
class Admin(db.Model):
	UTEID = db.StringProperty()	
	clearance = db.IntegerProperty()	#clearance level of the admin. 
	
class Instructor(db.Model):
	UTEID = db.StringProperty()	
	unique_id = db.IntegerProperty()	#unique_id of the class this instructor is teaching

class Applicant(db.Model):
	UTEID = db.StringProperty()	
	admission = db.DateProperty()
	degree = db.CategoryProperty()
	supervisor = db.StringProperty()	
	citizenship = db.CategoryProperty()
	native_english = db.CategoryProperty()
	history_comment = db.TextProperty()
	programming_comment = db.TextProperty()
	specializaion_comment = db.TextProperty()
	qualified_comment = db.TextProperty()
#End sub classes of User

class Course(db.Model):
	course_name = db.StringProperty()
	unique_id = db.IntegerProperty()		#Primary key
	instructor = db.StringProperty()
	numTA_assigned = db.IntegerProperty()
	semester = db.CategoryProperty()
	year = db.IntegerProperty()
	#finished = db.BooleanProperty(default=False)

#A course that is being setup for next semester is a subclass of Course
class Next_Sem_Course(db.Model):
	unique_id = db.IntegerProperty()
	wanted_comment = db.TextProperty()
	unwanted_comment = db.TextProperty()
	native_english = db.CategoryProperty()
	specialization_comment = db.TextProperty()
	expected_enrollment = db.IntegerProperty()
	numTA_needed = db.IntegerProperty()

#Tables for multivalued attributes
#Using the Multivalued attributes design pattern from the DB book
class App_Programming_Languages(db.Model):
	UTEID = db.StringProperty()
	langauge = db.StringProperty()
	
class App_History(db.Model):
	UTEID = db.StringProperty()
	course_name = db.StringProperty()
	
class App_Specializations(db.Model):
	UTEID = db.StringProperty()
	specialization = db.StringProperty()
	
class App_Qualified_Courses(db.Model):
	UTEID = db.StringProperty()
	course_name = db.StringProperty()

class Unwanted_Students(db.Model):
	unique_id = db.IntegerProperty()
	UTEID = db.StringProperty()

class Wanted_Students(db.Model):
	unique_id = db.IntegerProperty()
	UTEID = db.StringProperty()
	
