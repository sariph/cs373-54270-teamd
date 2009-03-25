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
				'phone_applicant'		: Validation.phone_number(value)
				'email_applicant'		: Validation.email(value)
				'comment_major'			: Validation.comment(value)
				'comment_admission'		: Validation.comment(value)
				'comment_phd'			: Validation.comment(value)
				'comment_supervising'		: Validation.comment(value)
				'comment_citizen'		: Validation.comment(value)
				'comment_native'		: Validation.comment(value)
				'comment_ta'			: Validation.comment(value)
				'comment_programming'		: Validation.comment(value)
				'comment_area'			: Validation.comment(value)
				'comment_qualified'		: Validation.comment(value)
			
				#Instructor Swicthes
				'comment_wanted'		: Validation.comment(value)
				'comment_unwanted'		: Validation.comment(value)
				'comment_native'		: Validation.comment(value)
				'comment_specialization'	: Validation.comment(value)
				#Admin switches	
				
				'comment_class_name'		: Validation.comment(value)
				'comment_inst_name'		: Validation.comment(value)
				'comment_exp_enrollment'	: Validation.comment(value)
				'comment_num_ta_needed'		: Validation.comment(value)
				'comment_num_ta_assigned'	: Validation.comment(value)
				
				
			}[key.split('_')[0]]()
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

