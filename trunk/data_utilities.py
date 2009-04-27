import os
import data_models

from datetime import date
from google.appengine.ext import db

def drop_all():
	db.delete(data_models.Users.all())
	db.delete(data_models.Phases.all())
	db.delete(data_models.Seasons.all())
	db.delete(data_models.Majors.all())
	db.delete(data_models.Specializations.all())
	db.delete(data_models.ProgrammingLanguages.all())
	db.delete(data_models.Instructors.all())
	db.delete(data_models.Admin.all())
	db.delete(data_models.Courses.all())
	db.delete(data_models.Applicants.all())
	db.delete(data_models.Semesters.all())
	db.delete(data_models.Classes.all())
	db.delete(data_models.Applications.all())
	db.delete(data_models.ApplicantsWanted.all())
	db.delete(data_models.ApplicantsUnwanted.all())
	db.delete(data_models.ApplicantsProgrammingLanguages.all())
	db.delete(data_models.ApplicantsCourses.all())
	db.delete(data_models.System.all())

def initialize():
	drop_all()

	global phase_initialization
	phase_initialization = insert_phase('initialization')
	insert_phase('applicants')
	insert_phase('instructors')
	insert_phase('matching')
	insert_phase('complete')

	global season_spring
	season_spring = insert_season('spring')
	insert_season('summer')
	global season_fall
	season_fall = insert_season('fall')

	admin = insert_admin('admin', 'pass', None, None)

	global semester_spring_2009
	semester_spring_2009 = insert_semester(phase_initialization, season_spring, 2009)

	global system
#	system = insert_system(None)
	system = insert_system(semester_spring_2009, None)
	return system

def load_test_data():
	initialize() # TODO: maybe hold on to this return value

	major_cs = insert_major('cs', 'Computer Science')
	major_ece = insert_major('ece', 'Computer Engineering')

	specialization_software_engineering = insert_specialization('software engineering')
	specialization_operating_systems = insert_specialization('operating systems')
	specialization_computer_vision = insert_specialization('computer vision')
	specialization_natural_language_processing = insert_specialization('natural language processing')
	specialization_parallel_computing = insert_specialization('parallel computing')
	specialization_microprocessor_and_vlsi_design = insert_specialization('microprocessor and VLSI design')
	specialization_theory = insert_specialization('theory')
	specialization_graphics = insert_specialization('graphics')
	specialization_networking = insert_specialization('networking')

	programming_language_java = insert_programming_language('java')
	programming_language_python = insert_programming_language('python')
	programming_language_c = insert_programming_language('c')
	programming_language_cpp = insert_programming_language('c++')
	programming_language_lisp = insert_programming_language('lisp')
	programming_language_pascal = insert_programming_language('pascal')
	programming_language_ruby = insert_programming_language('ruby')
	programming_language_perl = insert_programming_language('perl')
	programming_language_assembly = insert_programming_language('assembly')
	programming_language_visual_basic = insert_programming_language('visual basic')

	instructor_valmstrum = insert_instructor('valmstrum', 'pass', 'Vicki', 'Almstrum')
	instructor_dballard = insert_instructor('dballard', 'pass', 'Dana', 'Ballard')
	instructor_gdowning = insert_instructor('gdowning', 'pass', 'Glenn', 'Downing')
	instructor_rmooney = insert_instructor('rmooney', 'pass', 'Ray', 'Mooney')
	instructor_vrama = insert_instructor('vrama', 'pass', 'Vijaya', 'Ramachandran')
	instructor_wyoung = insert_instructor('wyoung', 'pass', 'William', 'Young')
	instructor_lalvisi = insert_instructor('lalvisi', 'pass', 'Lorenzo', 'Alvisi')
	instructor_dburger = insert_instructor('dburger', 'pass', 'Doug', 'Burger')
	instructor_dfussell = insert_instructor('dfussell', 'pass', 'Don', 'Fussell')
	instructor_mgouda = insert_instructor('mgouda', 'pass', 'Mohamed', 'Gouda')

	course_357H = insert_course(major_cs, '357H', 'Algorithms: Honors')
	course_361 = insert_course(major_cs, '361', 'Introduction to Computer Security')
	course_367 = insert_course(major_cs, '367', 'Numerical Methods')
	insert_course(major_cs, '369', 'Systems Modeling I')
	course_371P = insert_course(major_cs, '371P', 'Object-Oriented Programming')
	course_371R = insert_course(major_cs, '371R', 'Information Retrieval and Web Search')
	course_373 = insert_course(major_cs, '373', 'Software Engineering')
	course_378 = insert_course(major_cs, '378', 'Computational Brain-W')
	course_307 = insert_course(major_cs, '307', 'Foundations of Computer Science')
	course_315 = insert_course(major_cs, '315', 'Algorithms and Data Structures')
	insert_course(major_cs, '345', 'Programming Languages')
	insert_course(major_cs, '310', 'Computer Organization')
	course_372 = insert_course(major_cs, '372', 'Intro to Operating Systems')
	course_336 = insert_course(major_cs, '336', 'Analysis of Programs')
	course_302 = insert_course(major_cs, '302', 'Computer Fluency')
	# wasn't in test data, but is needed
	course_313k = insert_course(major_cs, '313k', 'Logic, Sets and Functions')
	course_341 = insert_course(major_cs, '341', 'Automata Theory')

	applicant_sbaggs = insert_applicant('sbaggs', 'pass', 'Steven', 'Baggs', db.PhoneNumber('512-232-9385'), db.Email('bags@cs.utexas.edu'), major_cs, date(2008, 9, 1), True, instructor_gdowning, True, True, specialization_software_engineering)
	applicant_jhiggins = insert_applicant('jhiggins', 'pass', 'Jessica', 'Higgins', db.PhoneNumber('512-345-9582'), db.Email('JH@cs.utexas.edu'), major_cs, date(2006, 9, 1), True, instructor_lalvisi, True, True, specialization_operating_systems)
	applicant_bmathews = insert_applicant('bmathews', 'pass', 'Bob', 'Mathews', db.PhoneNumber('408-849-9278'), db.Email('bobm@cs.utexas.edu'), major_cs, date(2007, 6, 2), False, instructor_dballard, True, True, specialization_computer_vision)
	applicant_aalagappan = insert_applicant('aalagappan', 'pass', 'Ahmadi', 'Alagappan', db.PhoneNumber('512-789-3709'), db.Email('aapan@hotmail.com'), major_cs, date(2004, 1, 20), True, instructor_rmooney, False, False, specialization_natural_language_processing)
	applicant_hhuntington = insert_applicant('hhuntington', 'pass', 'Henry', 'Huntington', db.PhoneNumber('202-968-0988'), db.Email('goodhunt@gmail.com'), major_ece, date(2008, 9, 1), True, instructor_gdowning, True, True, specialization_parallel_computing)
	applicant_akit = insert_applicant('akit', 'pass', 'Adriana', 'Kit', db.PhoneNumber('415-296-9782'), db.Email('akit@cs.utexas.edu'), major_cs, date(2009, 1, 20), False, None, False, False, None)
	applicant_nliu = insert_applicant('nliu', 'pass', 'Nancy', 'Liu', db.PhoneNumber('512-968-0294'), db.Email('liun@cs.utexas.edu'), major_ece, date(2002, 9, 1), True, instructor_dburger, False, False, specialization_microprocessor_and_vlsi_design)
	applicant_gkumar = insert_applicant('gkumar', 'pass', 'Gupta', 'Kumar', db.PhoneNumber('510-564-1205'), db.Email('gk@yahoo.com'), major_cs, date(2008, 9, 1), False, instructor_vrama, False, False, specialization_theory)
	applicant_pgiovanni = insert_applicant('pgiovanni', 'pass', 'Paolo', 'Giovanni', db.PhoneNumber('512-101-2492'), db.Email('pg13@cs.utexas.edu'), major_cs, date(2003, 1, 20), True, instructor_dfussell, False, False, specialization_graphics)
	applicant_mliz = insert_applicant('mliz', 'pass', 'Mona', 'Liz', db.PhoneNumber('512-129-4658'), db.Email('moonlit@hotmai.com'), major_cs, date(2000, 9, 1), True, instructor_mgouda, True, True, specialization_networking)

#	semester_spring_2009 = insert_semester(phase_initialization, season_spring, 2009)
	semester_fall_2008 = insert_semester(phase_initialization, season_fall, 2008)
	semester_spring_2008 = insert_semester(phase_initialization, season_spring, 2008)

	insert_class(course_373, semester_spring_2009, instructor_gdowning, 54265, 30, 1, None, None)
	insert_class(course_373, semester_spring_2009, instructor_gdowning, 54270, 30, 1, None, None)
	insert_class(course_378, semester_spring_2009, instructor_dballard, 54285, 30, 1, None, None)
	insert_class(course_361, semester_spring_2009, instructor_wyoung, 54230, 40, 2, None, None)
	insert_class(course_357H, semester_spring_2009, instructor_vrama, 54225, 15, 1, None, None)
	insert_class(course_371P, semester_fall_2008, instructor_gdowning, 55735, 50, 2, None, None)
	insert_class(course_373, semester_fall_2008, instructor_gdowning, 55754, 60, 2, None, None)
	insert_class(course_378, semester_spring_2008, instructor_dballard, 55750, 30, 1, None, None)
	insert_class(course_371R, semester_spring_2008, instructor_rmooney, 55720, 25, 1, None, None)
	insert_class(course_373, semester_spring_2008, instructor_valmstrum, 55740, 25, 1, None, None)

	insert_application(applicant_sbaggs, semester_spring_2009, None)
	insert_application(applicant_jhiggins, semester_spring_2009, None)
	insert_application(applicant_bmathews, semester_spring_2009, None)
	insert_application(applicant_aalagappan, semester_spring_2009, None)
	insert_application(applicant_hhuntington, semester_spring_2009, None)
	insert_application(applicant_akit, semester_spring_2009, None)
	insert_application(applicant_nliu, semester_spring_2009, None)
	insert_application(applicant_gkumar, semester_spring_2009, None)
	insert_application(applicant_pgiovanni, semester_spring_2009, None)
	insert_application(applicant_mliz, semester_spring_2009, None)

	insert_applicant_programming_language(applicant_sbaggs, programming_language_java)
	insert_applicant_programming_language(applicant_sbaggs, programming_language_python)
	insert_applicant_programming_language(applicant_jhiggins, programming_language_c)
	insert_applicant_programming_language(applicant_jhiggins, programming_language_cpp)
	insert_applicant_programming_language(applicant_jhiggins, programming_language_java)
	insert_applicant_programming_language(applicant_bmathews, programming_language_lisp)
	insert_applicant_programming_language(applicant_bmathews, programming_language_java)
	insert_applicant_programming_language(applicant_bmathews, programming_language_pascal)
	insert_applicant_programming_language(applicant_aalagappan, programming_language_lisp)
	insert_applicant_programming_language(applicant_aalagappan, programming_language_cpp)
	insert_applicant_programming_language(applicant_hhuntington, programming_language_ruby)
	insert_applicant_programming_language(applicant_hhuntington, programming_language_perl)
	insert_applicant_programming_language(applicant_hhuntington, programming_language_python)
	insert_applicant_programming_language(applicant_akit, programming_language_java)
	insert_applicant_programming_language(applicant_akit, programming_language_ruby)
	insert_applicant_programming_language(applicant_nliu, programming_language_c)
	insert_applicant_programming_language(applicant_nliu, programming_language_assembly)
	insert_applicant_programming_language(applicant_gkumar, programming_language_c)
	insert_applicant_programming_language(applicant_gkumar, programming_language_python)
	insert_applicant_programming_language(applicant_gkumar, programming_language_java)
	insert_applicant_programming_language(applicant_pgiovanni, programming_language_c)
	insert_applicant_programming_language(applicant_pgiovanni, programming_language_java)
	insert_applicant_programming_language(applicant_pgiovanni, programming_language_perl)
	insert_applicant_programming_language(applicant_mliz, programming_language_visual_basic)

	insert_applicant_course(applicant_sbaggs, course_373)
	insert_applicant_course(applicant_sbaggs, course_361)
	insert_applicant_course(applicant_jhiggins, course_307)
	insert_applicant_course(applicant_jhiggins, course_315)
	insert_applicant_course(applicant_bmathews, course_313k)
	insert_applicant_course(applicant_bmathews, course_378)
	insert_applicant_course(applicant_bmathews, course_371R)
	insert_applicant_course(applicant_aalagappan, course_315)
	insert_applicant_course(applicant_aalagappan, course_336)
	insert_applicant_course(applicant_aalagappan, course_357H)
	insert_applicant_course(applicant_hhuntington, course_302)
	insert_applicant_course(applicant_akit, course_373)
	insert_applicant_course(applicant_nliu, course_372)
	insert_applicant_course(applicant_nliu, course_367)
	insert_applicant_course(applicant_gkumar, course_341)
	insert_applicant_course(applicant_gkumar, course_367)
	insert_applicant_course(applicant_pgiovanni, course_373)
	insert_applicant_course(applicant_pgiovanni, course_361)

#	insert_system(semester_spring_2008)

def insert_phase(name):
	phase = db.GqlQuery('SELECT * FROM Phases WHERE name = :1', name).get()
	if phase is None:
		return db.get(data_models.Phases(name = name).put())
	else:
		phase.name = name
		return db.get(phase.put())

def insert_season(name):
	season = db.GqlQuery('SELECT * FROM Seasons WHERE name = :1', name).get()
	if season is None:
		return db.get(data_models.Seasons(name = name).put())
	else:
		season.name = name
		return db.get(season.put())

def insert_major(abbr, name):
	major = db.GqlQuery('SELECT * FROM Majors WHERE abbr = :1', abbr).get()
	if major is None:
		return db.get(data_models.Majors(abbr = abbr, name = name).put())
	else:
		major.abbr = abbr
		major.name = name
		return db.get(major.put())

def insert_specialization(name):
	specialization = db.GqlQuery('SELECT * FROM Specializations WHERE name = :1', name).get()
	if specialization is None:
		return db.get(data_models.Specializations(name = name).put())
	else:
		specialization.name = name
		return db.get(specialization.put())

def insert_programming_language(name):
	programming_language = db.GqlQuery('SELECT * FROM ProgrammingLanguages WHERE name = :1', name).get()
	if programming_language is None:
		return db.get(data_models.ProgrammingLanguages(name = name).put())
	else:
		programming_language.name = name
		return db.get(programming_language.put())

def insert_instructor(ut_eid, password, first_name, last_name):
	instructor = data_models.Instructors.gql('WHERE ut_eid = :1', ut_eid).get()
	if instructor is None:
		return db.get(data_models.Instructors(ut_eid = ut_eid, password = password, first_name = first_name, last_name = last_name).put())
	else:
		instructor.ut_eid = ut_eid
		instructor.password = password
		instructor.first_name = first_name
		instructor.last_name = last_name
		return db.get(instructor.put())

def insert_admin(ut_eid, password, first_name, last_name):
	admin = data_models.Admin.gql('WHERE ut_eid = :1', ut_eid).get()
	if admin is None:
		return db.get(data_models.Admin(ut_eid = ut_eid, password = password, first_name = first_name, last_name = last_name).put())
	else:
		admin.ut_eid = ut_eid
		admin.password = password
		admin.first_name = first_name
		admin.last_name = last_name
		return db.get(admin.put())

def insert_course(major, number, name):
	course = db.GqlQuery('SELECT * FROM Courses WHERE number = :1', number).get()
	if course is None:
		return db.get(data_models.Courses(major = major, number = number, name = name).put())
	else:
		course.major = major
		course.number = number
		course.name = name
		return db.get(course.put())

def insert_applicant(ut_eid, password, first_name, last_name, phone, email, major, admission, phd, supervising_professor, citizen, native_english_speaker, specialization):
	applicant = data_models.Applicants.gql('WHERE ut_eid = :1', ut_eid).get()
	if applicant is None:
		return db.get(data_models.Applicants(ut_eid = ut_eid, password = password, first_name = first_name, last_name = last_name, phone = phone, email = email, major = major, admission = admission, phd = phd, supervising_professor = supervising_professor, citizen = citizen, native_english_speaker = native_english_speaker, specialization = specialization).put())
	else:
		applicant.ut_eid = ut_eid
		applicant.password = password
		applicant.first_name = first_name
		applicant.last_name = last_name
		applicant.phone = phone
		applicant.email = email
		applicant.major = major
		applicant.admission = admission
		applicant.phd = phd
		applicant.supervising_professor = supervising_professor
		applicant.citizen = citizen
		applicant.native_english_speaker = native_english_speaker
		applicant.specialization = specialization
		return db.get(applicant.put())

def insert_semester(phase, season, year):
	year = date(int(year), 1, 1)
	semester = db.GqlQuery('SELECT * FROM Semesters WHERE season = :1 AND year = :2', season, year).get()
	if semester is None:
		return db.get(data_models.Semesters(phase = phase, season = season, year = year).put())
	else:
		semester.phase = phase
		semester.season = season
		semester.year = year
		return db.get(semester.put())

def insert_class(course, semester, instructor, unique, enrollment, tas_needed, native_english_speaker, background):
	_class = db.GqlQuery('SELECT * FROM Classes WHERE unique = :1', unique).get()
	if _class is None:
		return db.get(data_models.Classes(course = course, semester = semester, instructor = instructor, unique = unique, enrollment = enrollment, tas_needed = tas_needed, native_english_speaker = native_english_speaker, background = background).put())
	else:
		_class.course = course
		_class.semester = semester
		_class.instructor = instructor
		_class.unique = unique
		_class.enrollment = enrollment
		_class.tas_needed = tas_needed
		_class.native_english_speaker = native_english_speaker
		_class.background = background
		return db.get(_class.put())

def insert_application(applicant, semester, assigned_class):
	application = db.GqlQuery('SELECT * FROM Applications WHERE applicant = :1 AND semester = :2', applicant, semester).get()
	if application is None:
		return db.get(data_models.Applications(applicant = applicant, semester = semester, assigned_class = assigned_class).put())
	else:
		application.applicant = applicant
		application.semester = semester
		application.assigned_class = assigned_class
		return db.get(application.put())

def insert_applicant_wanted(applicant, class_in_question):
	applicant_wanted = db.GqlQuery('SELECT * FROM ApplicantsWanted WHERE applicant = :1 AND class_in_question = :2', applicant, class_in_question).get()
	if applicant_wanted is None:
		return db.get(data_models.ApplicantsWanted(applicant = applicant, class_in_question = class_in_question).put())
	else:
		applicant_wanted.applicant = applicant
		applicant_wanted.class_in_question = class_in_question
		return db.get(applicant_wanted.put())

def insert_applicant_unwanted(applicant, class_in_question):
	applicant_unwanted = db.GqlQuery('SELECT * FROM ApplicantsUnwanted WHERE applicant = :1 AND class_in_question = :2', applicant, class_in_question).get()
	if applicant_unwanted is None:
		return db.get(data_models.ApplicantsUnwanted(applicant = applicant, class_in_question = class_in_question).put())
	else:
		applicant_unwanted.applicant = applicant
		applicant_unwanted.class_in_question = class_in_question
		return db.get(applicant_unwanted.put())

def insert_applicant_programming_language(applicant, programming_language):
	applicant_programming_language = db.GqlQuery('SELECT * FROM ApplicantsProgrammingLanguages WHERE applicant = :1 AND programming_language = :2', applicant, programming_language).get()
	if applicant_programming_language is None:
		return db.get(data_models.ApplicantsProgrammingLanguages(applicant = applicant, programming_language = programming_language).put())
	else:
		applicant_programming_language.applicant = applicant
		applicant_programming_language.programming_language = programming_language
		return db.get(applicant_programming_language.put())

def insert_applicant_course(applicant, course):
	applicant_course = db.GqlQuery('SELECT * FROM ApplicantsCourses WHERE applicant = :1 AND course = :2', applicant, course).get()
	if applicant_course is None:
		return db.get(data_models.ApplicantsCourses(applicant = applicant, course = course).put())
	else:
		applicant_course.applicant = applicant
		applicant_course.course = course
		return db.get(applicant_course.put())

def insert_system(current_semester, current_user):
	system = data_models.System.all().get()
	if system is None:
		return db.get(data_models.System(current_semester = current_semester, current_user = current_user).put())
	else:
		system.current_semester = current_semester
		system.current_user = current_user
		return db.get(system.put())

