import cgi

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class User(polymodel.PolyModel):
	first_name = db.StringProperty()
	last_name = db.StringProperty()
	middle_name = db.StringProperty()
	UTEID = db.StringProperty()
	password = db.StringProperty()
	phone = db.PhoneNumberProperty()
	email = db.EmailProperty()
	position = db.CategoryProperty()
	
class Applicant(User):
	admission = db.DateProperty()
	degree = db.CategoryProperty()
	supervisor = db.StringProperty()	#A foreign key. Many to One relation between applicants and instructors
	citizenship = db.CategoryProperty()
	native_english = db.CategoryProperty()
	history_comment = db.TextProperty()
	programming_comment = db.TextProperty()
	specializaion_comment = db.TextProperty()
	qualified_comment = db.TextProperty()

#Tables for TA information, indexed by UTEID
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
	
#The real life system would have many more distinguishing features for the instructor subclass
class Instructor(User):
	tenure = db.CategoryProperty()
	accepted = db.DateProperty()

class Course(db.Model):
	course_name = db.StringProperty()
	unique_id = db.IntegerProperty()
	instructor = db.StringProperty()
	wanted_comment = db.TextProperty()
	unwanted_comment = db.TextProperty()
	native_english = db.CategoryProperty()
	specialization_comment = db.TextProperty()
	expected_enrollment = db.IntegerProperty()
	numTA_needed = db.IntegerProperty()
	numTA_assigned = db.IntegerProperty()
	semester = db.CategoryProperty()
	year = db.IntegerProperty()
	finished = db.BooleanProperty()
	
class Unwanted_Students(db.Model):
	unique_id = db.IntegerProperty()
	UTEID = db.StringProperty()

class Wanted_Students(db.Model):
	unique_id = db.IntegerProperty()
	UTEID = db.StringProperty()
	
class TA_assignments(db.Model):
	unique_id = db.IntegerProperty()
	UTEID = db.StringProperty()
	
class Admin(db.Model):
	UTEID = db.StringProperty()
	clearance = db.IntegerProperty()