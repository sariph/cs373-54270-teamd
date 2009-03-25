import re

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
				'name'     : lambda: True if re.match('.+', value) else False,
				'password' : lambda: True if re.match('.{6,30}', value) else False,
				'address'  : lambda: True if re.match('.+', value) else False,
				'phone'    : lambda: True if re.match('.+', value) else False,
				# lol, this is ALMOST to RFC 2822, doesn't handle double quoted sections before '@' or square bracket Internet address after, perfect bug op
				'email'    : lambda: True if re.match('[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?', value) else False,
				'comment'  : lambda: True if re.match('.+', value) else False,
			}[key.split('_')[0]]()
			result['valid'] = True if ghetto_switch else False
			self.results.append(result)

