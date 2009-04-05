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
	position = db.StringProperty()		#Undergraduate, Graduate, Professor, etc.
	
#Subclasses of User. Using the Relational scheme from the DB book
class TA(db.Model):
	UTEID = db.StringProperty()	
	class_id = db.IntegerProperty()		#class_id the TA is assigned to
	
class Admin(db.Model):
	UTEID = db.StringProperty()	
	clearance = db.IntegerProperty()	#clearance level of the admin. 
	
class Instructor(db.Model):
	UTEID = db.StringProperty()	
	class_id = db.IntegerProperty()		#class_id the Instructor is teaching

class Instructor_App(db.Model):
	UTEID = db.StringProperty()	
	class_id = db.IntegerProperty()		#class_id the Professor wishes to teach

class Applicant(db.Model):
	UTEID = db.StringProperty()	
	admission = db.DateProperty()
	degree = db.StringProperty()
	supervisor = db.StringProperty()	
	citizenship = db.StringProperty()
	native_english = db.BooleanProperty()
	history_comment = db.TextProperty()
	programming_comment = db.TextProperty()
	specializaion_comment = db.TextProperty()
	qualified_comment = db.TextProperty()
#End sub classes of User

class Class(db.Model):
	class_id = db.StringProperty()		#This is a combination of Unique id, semester, and year. Ex: 56025fall2000. This is the primary key
	course_name = db.StringProperty()
	unique_id = db.IntegerProperty()
	instructor = db.StringProperty()
	semester = db.StringProperty()
	year = db.IntegerProperty()
	wanted_comment = db.TextProperty()
	unwanted_comment = db.TextProperty()
	native_english = db.StringProperty()
	specialization_comment = db.TextProperty()
	expected_enrollment = db.IntegerProperty()
	numTA_needed = db.IntegerProperty()

#Tables for multivalued attributes
#Using the Multivalued attributes design pattern from the DB book
class App_Programming_Language(db.Model):
	UTEID = db.StringProperty()
	langauge = db.StringProperty()
	
class App_History(db.Model):
	UTEID = db.StringProperty()
	course_name = db.StringProperty()
	
class App_Specialization(db.Model):
	UTEID = db.StringProperty()
	specialization = db.StringProperty()
	
class App_Qualified_Course(db.Model):
	UTEID = db.StringProperty()
	course_name = db.StringProperty()

class Class_Specialization(db.Model):
	class_id = db.StringProperty()
	specialization = db.StringProperty()

class Unwanted_Student(db.Model):
	class_id = db.IntegerProperty()
	UTEID = db.StringProperty()

class Wanted_Student(db.Model):
	class_id = db.IntegerProperty()
	UTEID = db.StringProperty()
	
#Table for programming langauges. Admin can add or remove from it
#The applicants select from a collection of checkboxes of these
class Programming_Language(db.Model):
	language = db.StringProperty()
	
#Table for course names. Admin can add or remove from it
#The applicants select from a collection of checkboxes of these
#Classes are instances of these courses that the admin can create
class Course_Name(db.Model):
	course_name = db.StringProperty()
	
#Table for majors. Admin can add or remove from it
#The applicants select from a drop down box of these
class Major(db.Model):
	major = db.StringProperty()
	
#Table for specializations. Admin can add or remove from it
#The applicants select from a group of check boxes for these
class Specialization(db.Model):
	specialization = db.StringProperty()