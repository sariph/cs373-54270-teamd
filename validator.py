import re
import Validation

class Validator:
	def __init__(self, form_data):
		self.results = []

		#TODO: how would this happen?
#		if not form_data:
#			self.valid = False
#			self.errors.append('You POSTed without data.')

		for key, value in form_data:
			result = {}
			result['key'] = key
			result['value'] = value
			ghetto_switch = {
				#'name'     : Validation.name(value),
				#'password' : lambda: True if re.match('.{6,30}', value) else False,
				#'address'  : lambda: True if re.match('.+', value) else False,
				#'phone'    : Validation.phone_number(value),
				# lol, this is ALMOST to RFC 2822, doesn't handle double quoted sections before '@' or square bracket Internet address after, perfect bug op
				#'email'    : Validation.email(value),
				#'comment'  : lambda: True if re.match('.+', value) else False,
				
				#TA Applicant switches
				'phone_applicant'		: lambda x: Validation.phone_number(x),
				'email_applicant'		: lambda x: Validation.email(x),
				'comment_major'			: lambda x: Validation.comment(x),
				'comment_admission'		: lambda x: Validation.date(x),
				'comment_phd'			: lambda x: Validation.degree_type(x),
				'comment_supervising'		: lambda x: Validation.comment(x),
				'comment_citizen'		: lambda x: Validation.citizen(x),
				'comment_native'		: lambda x: Validation.yes_no(x),
				'comment_ta'			: lambda x: Validation.yes_no(x),
				'comment_programming'		: lambda x: Validation.comment(x),
				'comment_area'			: lambda x: Validation.comment(x),
				'comment_qualified'		: lambda x: Validation.comment(x),
			
				#Instructor Swicthes
				'comment_wanted'		: lambda x: Validation.comment(x),
				'comment_unwanted'		: lambda x: Validation.comment(x),
				'comment_native'		: lambda x: Validation.comment(x),
				'comment_specialization'	: lambda x: Validation.comment(x),
				#Admin switches	
				
				'comment_class_name'		: lambda x: Validation.comment(x),
				'comment_inst_name'		: lambda x: Validation.comment(x),
				'comment_exp_enrollment'	: lambda x: Validation.comment(x),
				'comment_num_ta_needed'		: lambda x: Validation.comment(x),
				'comment_num_ta_assigned'	: lambda x: Validation.comment(x),
				
				
			}[key](value)
			
			result['valid'] = True if ghetto_switch else False
			self.results.append(result)

#		for key, value in form_data:
#			result = {}
#			result['key'] = key
#			result['value'] = value
#			ghetto_switch = {
#				'name'     : lambda: True if re.match('.+', value) else False,
#				'password' : lambda: True if re.match('.{6,30}', value) else False,
#				'address'  : lambda: True if re.match('.+', value) else False,
#				'phone'    : lambda: True if re.match('.+', value) else False,
#				# lol, this is ALMOST to RFC 2822, doesn't handle double quoted sections before '@' or square bracket Internet address after, perfect bug op
#				'email'    : lambda: True if re.match('[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?', value) else False,
#				'comment'  : lambda: True if re.match('.+', value) else False,
#			}[key.split('_')[0]]()
#			result['valid'] = True if ghetto_switch else False
#			self.results.append(result)

