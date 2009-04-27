import re
import time

class Validator:
	"""
	Generic validator class depending on form type.
	"""
	def __init__(self, form_data):
		"""
		Constructor validates k-v pairs found in form_data and returns results.
		"""
		self.results = []

		#TODO: how would this happen?
		#if not form_data:
			#self.valid = False
			#self.errors.append('You POSTed without data.')

		for key, value in form_data.items():
			result = {}
			result['key'] = key
			result['value'] = value
			try:
				ghetto_switch = {
					'email'		: lambda x: self.email(x),
					'password'	: lambda x: self.comment(x),
					'ut_eid'	: lambda x: self.comment(x),
					'select'	: lambda x: self.comment(x),
					'radio'		: lambda x: self.comment(x),
					'year'		: lambda x: self.year(x),
					'abbr'		: lambda x: self.abbr(x),
					'phone'		: lambda x: self.phone(x),
					'date'		: lambda x: self.comment(x),
					'boolean'	: lambda x: self.boolean(x),
					'unique'	: lambda x: self.unique(x),
					'number'	: lambda x: self.number(x),
					'comment'	: lambda x: self.comment(x),
#					'yesno'		: lambda x: Validation.yes_no(x),
#					'text'		: lambda x: True,
#					'optional'	: lambda x: True,
#					'degree'	: lambda x: Validation.degree_type(x),
#					'citizen'	: lambda x: Validation.citizen(x),
#					'comment_phase' : lambda x: Validation.number(x),
#					'radio_phase' 	: lambda x: Validation.number(x),
#					'courseid'	: lambda x: Validation.validCourseID(x),
#					'coursename'	: lambda x: Validation.validCourseName(x),

					#TA Applicant switches
					#'phone_applicant'		: lambda x: Validation.phone_number(x),
					#'email_applicant'		: lambda x: Validation.email(x),
					#'comment_major'			: lambda x: Validation.comment(x),
					#'comment_admission'		: lambda x: Validation.date(x),
					#'comment_phd'			: lambda x: Validation.degree_type(x),
					#'comment_supervising'		: lambda x: Validation.comment(x),
					#'comment_citizen'		: lambda x: Validation.citizen(x),
					#'comment_native'		: lambda x: Validation.yes_no(x),
					#'comment_ta'			: lambda x: Validation.yes_no(x),
					#'comment_programming'		: lambda x: Validation.comment(x),
					#'comment_area'			: lambda x: Validation.comment(x),
					#'comment_qualified'		: lambda x: Validation.comment(x),
	
					#Instructor Swicthes
					#'comment_wanted'		: lambda x: Validation.comment(x),
					#'comment_unwanted'		: lambda x: Validation.comment(x),
					#'comment_native'		: lambda x: Validation.yes_no(x),
					#'comment_specialization'	: lambda x: Validation.comment(x),
	
					#Admin switches	
					#'comment_class_name'		: lambda x: Validation.comment(x),
					#'comment_inst_name'		: lambda x: Validation.comment(x),
					#'comment_exp_enrollment'	: lambda x: Validation.number(x),
					#'comment_num_ta_needed'	: lambda x: Validation.number(x),
					#'comment_num_ta_assigned'	: lambda x: Validation.number(x),
				}[key.split('|')[0]](value)
			except KeyError:
				result['valid'] = False

			result['valid'] = True if ghetto_switch else False
			self.results.append(result)

	def email(self, s):
		"""
		Email validator. This is ALMOST to RFC 2822, doesn't handle double quoted sections before '@' or square bracket Internet address after, perfect bug op
		"""
		return re.search('^[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?$', s) is not None

	def year(self, s):
		"""
		Year validator
		"""
		return re.search('^(1|2)(9|0|1)[0-9][0-9]$', s) is not None

	def abbr(self, s):
		"""
		Validates any abbreviation
		"""
		return re.search('^(\w|\s){2,3}$', s) is not None

	def phone(self, s):
		"""
		Phone number validator.
		"""
		return re.search('^(\d{3}-)?\d{3}-\d{4}$', s) is not None

	def boolean(self, s):
		"""
		Boolean validator.
		"""
		return re.search('^((t|T)rue|(f|F)alse)$', s) is not None

	def unique(self, s):
		"""
		Number validator.
		"""
		return re.search('^\d{5}$',s) is not None

	def number(self, s):
		"""
		Number validator.
		"""
		return re.search('^\d+$', s) is not None

	def comment(self, s):
		"""
		Comment validator.
		"""
		return re.search('.+', s) is not None

'''
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

	def validSpecialization (s) :
		#depends on query results
		return not empty(s)

	def validSupervisor (s) :
		#depends on query results
		return not empty(s)

	def validNativeEnglish (s) :
		return not re.search('(Yes|No)',s) is None

	def validComment (s) :
		return comment(s) #always returns true since they're optional

	def validCourseID (s) :
		#depends on query results
		return (re.search('^([A-Z])+(\d\d\d)([a-z])*$', s) is not None)

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

	def validExpectedEnrollment (s) :
		#return not re.search('[0-9]+',s) is None
		if s > 0:
			return True
		return False

	def validLanguage (s) :
		#depends on query results
		return not empty(s)

	def validCourseName (s) :
		#depends on query results
		return (re.search('^([A-Z](\w)*(\s)*)+$', s) is not None)

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
		elif not validComment(applicant.history_comment):
			return False
		elif not validComment(applicant.programming_comment):
			return False
		elif not validComment(applicant.specialization_comment):
			return False
		elif not validComment(applicant.qualified_comment):
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
		elif not validComment(c.wanted_comment):
			return False
		elif not validComment(c.unwanted_comment):
			return False
		elif not validNativeEnglish(c.native_english):
			return False
		elif not validComment(c.specialization_comment):
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
'''

