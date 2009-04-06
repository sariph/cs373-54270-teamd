#!/usr/bin/env python

import re
import time

def phone_number (s) :
	"""
	Phone number validator.
	"""
	return not re.search('^(\d\d\d-)?\d\d\d-\d\d\d\d$', s) is None

def phone_number_ext (s) :
	"""
	Phone number extension validator.
	"""
	return not re.search('^(\d)*$',s) is None

def email (s) :
	"""
	E-mail address validator.
	"""
	return not re.search('(^(\w|\-|\_)(\+)?((\.)?(\w|\-|\_)+)*)\@(\w)+(\-|\w)*(\w)+((\.)?(\w)+(\-|\w)*(\w)+)*\.(com|net|org|gov|edu|info|biz|us)$', s) is None

def date (s) :
	"""
	Date validator.
	"""
	result = False
	#Feb
	if(not re.search('^(02)\-((0[1-9])|((1|2)(\d)))\-[0-9][0-9][0-9][0-9]$',s) is None): return True
	#Jan, Mar, May...
	if(not re.search('^(01|03|05|07|08|10|12)\-(30|31|(((0[1-9])|((1|2)(\d)))))\-[0-9][0-9][0-9][0-9]$',s) is None): return True
	#Apr, Jun, Sep, Nov
	if(not re.search('^(04|06|09|11)\-(30|(((0[1-9])|((1|2)(\d)))))\-[0-9][0-9][0-9][0-9]$',s) is None): return True
	return False

def name (s) :
	"""
	Name validator.
	"""
	return not re.search('^^([A-Z]([a-zA-Z]*(\-|\')?[a-zA-Z]*[a-zA-Z](\')?)*(\s)?)+$',s) is None

def class_number (s) :
	"""
	Class number validator.
	"""
	return not re.search('(^cs\d\d\d)|(^CS\d\d\d)',s) is None

def number (s) :
	"""
	Number validator.
	"""
	return not re.search('^(\d)+$',s) is None

def unique (s) :
	"""
	Number validator.
	"""
	#return not re.search('^(\d)(\d)(\d)(\d)(\d)$',s) is None
	return s >= 0 and s < 100000

def comment (s) :
	"""
	Comment validator.
	"""
	return not re.search('.+',s) is None

def degree_type (s) :
	"""
	Degree validator.
	"""
	return not re.search('^(PhD|Masters)$',s) is None

def citizen (s) :
	"""
	Resident/Citizen validator.
	"""
	return not re.search('^(Citizen|Resident)$',s) is None

def yes_no (s) :
	"""
	yes/no validator.
	"""
	return not re.search('^(yes|no)$',s) is None

def empty (s) :
	return re.search('.+',s) is None


def validUTEID (s) :
	return not empty(s)

def validPassword (s) :
	return not empty(s)

def validPosition (s) :
	return not re.search('(Undergraduate|Graduate|Professor)',s) is None

def validClearance (s) :
	return not empty(s)




def validMajor (s) :
	#depends on query results
	return not empty(s)

def validAdmission (s) :
	return date(s)

def validSupervisor (s) :
	#depends on query results
	return not empty(s)

def validNativeEnglish (s) :
	return not re.search('(Yes|No)',s) is None

def validHistoryComment (s) :
	return True

def validProgrammingComment (s) :
	return True

def validQualifiedComment (s) :
	return True


def validCourseID (s) :
	#depends on query results
	return not empty(s)

def validInstructor (s) :
	#depends on query results
	return not empty(s)

def validSemester (s) :
	return not re.search('(Spring|Summer|Fall)',s) is None

def validYear (s) :
	#return not re.search('([19]|[20])[0-9][0-9]',s) is None
	#valid years are between 1900 and current year
	try:
		return int(s) >= 1900 and int(s) <= time.localtime(time.time())[0]
	except ValueError:
		return False

def validWantedComment (s) :
	return True

def validUnwantedComment (s) :
	return True

def validExpectedEnrollment (s) :
	#return not re.search('[0-9]+',s) is None
	if s > 0:
		return True
	return False

def validLanguage (s) :
	#depends on query results
	return not empty(s)

def validSpecializationComment (s) :
	return True

def validCourseName (s) :
	#depends on query results
	return not empty(s)

def UserDataValidator(user):
	"""
	Validates every field in User
	"""
	if not validUTEID(user.UTEID):
		return False
	elif not name(user.first_name):
		return False
	elif not name(user.last_name):
		return False
	elif not validPassword(user.password):
		return False
	elif not phone_number(user.phone):
		return False
	elif not email(user.email):
		return False
	elif not validPosition(user.position):
		return False
	return True



def TADataValidator(ta):
	"""
	Validates every field of TA
	"""
	if not validUTEID(ta.UTEID):
		return False
	if not class_number(ta.class_id):
		return False
	return True

def AdminDataValidator(admin):
	"""
	Validates every field of Admin 
	"""
	if not validUTEID(admin.UTEID):
		return False
	if not validClearance(admin.clearance):
		return False
	return True

def InstructorDataValidator(instructor):
	"""
	Validates every field of Intructor 
	"""
	if not validUTEID(instructor.UTEID):
		return False
	if not class_number(instructor.class_id):
		return False

	return True

def InstructorApplicantDataValidator(instructorApplicant):
	"""
	Validates every field of Intructor 
	"""
	if not validUTEID(instructorApplicant.UTEID):
		return False
	if not class_number(instructorApplicant.class_id):
		return False

	return True

def ApplicantDataValidator(applicant):
	"""
	Validates applicant form	
	"""
	if not validUTEID(applicant.UTEID):
		return False
	elif not validMajor(applicant.major):
		return False
	elif not validAdmission(applicant.admission):
		return False
	elif not degree_type(applicant.degree):
		return False
	elif not validSupervisor(applicant.supervisor):
		return False
	elif not citizen(applicant.citizenship):
		return False
	elif not validNativeEnglish(applicant.native_english):
		return False
	elif not validHistoryComment(applicant.history_comment):
		return False
	elif not validProgrammingComment(applicant.programming_comment):
		return False
	elif not validSpecializationComment(applicant.specialization_comment):
		return False
	elif not validQualifiedComment(applicant.qualified_comment):
		return False
	return True


def ClassDataValidator(c):
	"""
	"""
	if not class_number(c.class_id):
		return False
	elif not validCourseID(c.course_id):
		return False
	elif not unique(c.unique_id):
		return False
	elif not validInstructor(c.instructor):
		return False
	elif not validSemester(c.semester):
		return False
	elif not validYear(c.year):
		return False
	elif not validWantedComment(c.wanted_comment):
		return False
	elif not validUnwantedComment(c.unwanted_comment):
		return False
	elif not validNativeEnglish(c.native_english):
		return False
	elif not validSpecializationComment(c.specialization_comment):
		return False
	elif not validExpectedEnrollment(c.expected_enrollment):
		return False
	elif not validExpectedEnrollment(c.numTA_needed):
		return False
	return True


def AppProgrammingLanguageDataValidator(applicantProgLang):
	if not validUTEID(applicantProgLang.UTEID):
		return False
	elif not validLanguage(applicantProgLang.language):
		return False
	return True

def AppHistoryDataValidator(applicantHistory):
	if not validUTEID(applicantHistory.UTEID):
		return False
	elif not validCourseID(applicantHistory.course_id):
		return False
	return True
def AppSpecializationDataValidator(applicantSpecialization):
	if not validUTEID(applicantSpecialization.UTEID):
		return False
	elif not validSpecialization(applicantSpecialization.specialization):
		return False
	return True

def AppQualifiedCourseDataValidator(applicantQualCourse):
	if not validUTEID(applicantQualCourse.UTEID):
		return False
	elif not validCourseID(applicantQualCourse.course_id):
		return False
	return True


def requestedSpecDataValidator(requestedSpec):
	if not class_number(requestedSpec.class_id):
		return False
	elif not validSpecialization(requestedSpec.specialization):
		return False
	return True

def unwantedStudentDataValidator(unwantedStudent):
	if not class_number(unwantedStudent.class_id):
		return False
	elif not validUTEID(unwantedStudent.UTEID):
		return False
	return True

def wantedStudentDataValidator(wantedStudent):
	if not class_number(wantedStudent.class_id):
		return False
	elif not validUTEID(wantedStudent.UTEID):
		return False
	return True

def progLangDataValidator(progLang):
	if not validLanguage(progLang.language):
		return False
	return True

def courseDataValidator(course):
	if not validCourseName(course.course_name):
		return False
	elif not validCourseID(course.course_id):
		return False
	return True

def majorDataValidator(major):
	if not validMajor(major.major):
		return False
	return True

def specializationDataValidator(specialization):
	return True
