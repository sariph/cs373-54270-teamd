from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class User(db.Model):
	"""
	entries represent abstract users
	"""
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
	"""
	subclass of User, entries represents TAs
	"""
	UTEID = db.StringProperty()
	class_id = db.StringProperty()		#class_id the TA is assigned to

class Admin(db.Model):
	"""
	subclass of User, entries represent administrators
	"""
	UTEID = db.StringProperty()
	clearance = db.IntegerProperty()	#clearance level of the admin. 

class Instructor(db.Model):
	"""
	subclass of User, entries represent instructors
	"""
	UTEID = db.StringProperty()
	class_id = db.StringProperty()		#class_id the Instructor is teaching

class Instructor_App(db.Model):
	"""
	subclass of User, entries represent instructor applicants
	"""
	UTEID = db.StringProperty()
	course_id = db.StringProperty()		#class_id the Professor wishes to teach

class Applicant(db.Model):
	"""
	subclass of User, entries represent applicants
	"""
	UTEID = db.StringProperty()
	major = db.StringProperty()
	admission = db.StringProperty()
	degree = db.StringProperty()
	supervisor = db.StringProperty()
	citizenship = db.StringProperty()
	native_english = db.StringProperty()		#"Yes" or "No"
	history_comment = db.TextProperty()
	programming_comment = db.TextProperty()
	specialization_comment = db.TextProperty()
	qualified_comment = db.TextProperty()
#End sub classes of User

class Class(db.Model):
	"""
	entries represent classes
	"""
	class_id = db.StringProperty()		#This is a combination of Unique id, semester, and year. Ex: 56025fall2000. This is the primary key
	course_id = db.StringProperty()
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
	"""
	table for multivalued attributes
	"""
	UTEID = db.StringProperty()
	language = db.StringProperty()

class App_History(db.Model):
	"""
	table for multivalued attributes
	"""
	UTEID = db.StringProperty()
	course_id = db.StringProperty()

class App_Specialization(db.Model):
	"""
	table for multivalued attributes
	"""
	UTEID = db.StringProperty()
	specialization = db.StringProperty()

class App_Qualified_Course(db.Model):
	"""
	table for multivalued attributes
	"""
	UTEID = db.StringProperty()
	course_id = db.StringProperty()

class Requested_Specialization(db.Model):
	"""
	table for multivalued attributes
	"""
	class_id = db.StringProperty()
	specialization = db.StringProperty()

class Unwanted_Student(db.Model):
	"""
	table for multivalued attributes
	"""
	class_id = db.StringProperty()
	UTEID = db.StringProperty()

class Wanted_Student(db.Model):
	"""
	table for multivalued attributes
	"""
	class_id = db.StringProperty()
	UTEID = db.StringProperty()

#Table for programming langauges. Admin can add or remove from it
#The applicants select from a collection of checkboxes of these
class Programming_Language(db.Model):
	"""
	entries represent programming languages
	"""
	language = db.StringProperty()

#Table for courses Admin can add or remove from it
#The applicants select from a collection of checkboxes of these
#Classes are instances of these courses that the admin can create
class Course(db.Model):
	"""
	entries represent courses
	"""
	course_name = db.StringProperty()
	course_id = db.StringProperty()

#Table for majors. Admin can add or remove from it
#The applicants select from a drop down box of these
class Major(db.Model):
	"""
	entries represent majors
	"""
	major = db.StringProperty()

#Table for specializations. Admin can add or remove from it
#The applicants select from a group of check boxes for these
class Specialization(db.Model):
	"""
	entries represent specializations
	"""
	specialization = db.StringProperty()

