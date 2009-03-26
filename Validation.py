#!/usr/bin/env python

import re

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
	return not re.search('^(citizen|resident)$',s) is None

def yes_no (s) :
	"""
	yes/no validator.
	"""
	return not re.search('^(yes|no)$',s) is None
