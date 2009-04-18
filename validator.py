import re
import Validation

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

		for key, value in form_data:
			result = {}
			result['key'] = key
			result['value'] = value
			try:
				ghetto_switch = {
					#'email'    : lambda: True if re.match('[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?', value) else False,
					# lol, this is ALMOST to RFC 2822, doesn't handle double quoted sections before '@' or square bracket Internet address after, perfect bug op
	
					'phone'		: lambda x: Validation.phone_number(x),
					'email'		: lambda x: Validation.email(x),
					'date'		: lambda x: Validation.date(x),
					'comment'	: lambda x: Validation.comment(x),
					'radio'		: lambda x: Validation.comment(x),
					'number'	: lambda x: Validation.number(x),
					'unique'	: lambda x: Validation.unique(x),
					'yesno'		: lambda x: Validation.yes_no(x),
					'text'		: lambda x: True,
					'optional'	: lambda x: True,
					'uniqueUTEID'	: lambda x: Validation.comment(x),
					'degree'	: lambda x: Validation.degree_type(x),
					'citizen'	: lambda x: Validation.citizen(x),
                                        'comment_phase' : lambda x: Validation.number(x)
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
				}[key.split('_')[0]](value)
			except:
				result['valid'] = True

			result['valid'] = True if ghetto_switch else False
			self.results.append(result)
