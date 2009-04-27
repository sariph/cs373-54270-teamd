from google.appengine.ext import db
from google.appengine.ext.db import polymodel

# PolyModels

class Users (polymodel.PolyModel):
	ut_eid = db.StringProperty()
	password = db.StringProperty()
	first_name = db.StringProperty()
	last_name = db.StringProperty()

# Purely Accessory tables

class Phases (db.Model):
	name = db.StringProperty()

class Seasons (db.Model):
	name = db.StringProperty()

class Majors (db.Model):
	abbr = db.StringProperty()
	name = db.StringProperty()

class Specializations (db.Model):
	name = db.StringProperty()

class ProgrammingLanguages (db.Model):
	name = db.StringProperty()

class Instructors (Users):
	pass
#	ut_eid = db.StringProperty()
#	password = db.StringProperty()
#	first_name = db.StringProperty()
#	last_name = db.StringProperty()

class Admin (Users):
	pass

# Combination tables

class Courses (db.Model):
	major = db.ReferenceProperty(Majors)
	number = db.StringProperty() # I know it says number, but I used a StringProperty because the official schedule does the same (i.e. '313k')
	name = db.StringProperty()

class Applicants (Users):
#	ut_eid = db.StringProperty()
#	password = db.StringProperty()
#	first_name = db.StringProperty()
#	last_name = db.StringProperty()
	phone = db.PhoneNumberProperty()
	email = db.EmailProperty()
	major = db.ReferenceProperty(Majors)
	admission = db.DateProperty()
	phd = db.BooleanProperty()
	supervising_professor = db.ReferenceProperty(Instructors)
	citizen = db.BooleanProperty()
	native_english_speaker = db.BooleanProperty()
	specialization = db.ReferenceProperty(Specializations)

class Semesters (db.Model):
	phase = db.ReferenceProperty(Phases)
	season = db.ReferenceProperty(Seasons)
	year = db.DateProperty()

class Classes (db.Model):
	course = db.ReferenceProperty(Courses)
	semester = db.ReferenceProperty(Semesters)
	instructor = db.ReferenceProperty(Instructors)
	unique = db.IntegerProperty()
	enrollment = db.IntegerProperty()
	tas_needed = db.IntegerProperty()
	native_english_speaker = db.BooleanProperty()
	background = db.ReferenceProperty(Specializations)

# Purely join tables

class Applications (db.Model):
	applicant = db.ReferenceProperty(Applicants)
	semester = db.ReferenceProperty(Semesters)
	assigned_class = db.ReferenceProperty(Classes)

class ApplicantsWanted (db.Model):
	applicant = db.ReferenceProperty(Applicants)
	class_in_question = db.ReferenceProperty(Classes) # TODO: better name

class ApplicantsUnwanted (db.Model):
	applicant = db.ReferenceProperty(Applicants)
	class_in_question = db.ReferenceProperty(Classes) # TODO: better name

class ApplicantsProgrammingLanguages (db.Model):
	applicant = db.ReferenceProperty(Applicants)
	programming_language = db.ReferenceProperty(ProgrammingLanguages)

class ApplicantsCourses (db.Model):
	applicant = db.ReferenceProperty(Applicants)
	course = db.ReferenceProperty(Courses)

# only non-plural class because it will only contain one row
class System (db.Model):
	current_semester = db.ReferenceProperty(Semesters)
	current_user = db.ReferenceProperty(Users)

