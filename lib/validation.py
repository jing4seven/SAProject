'''
Static function tools for validation in serilizer 
'''
import re

def check_char_basic(field_value="", min_length=5, max_length=50):
	'''
	Basic char field checking function.

	Before invoke this function, you should trim white space.
	This function just only alow alphab, blank and numeric.

	'''
	pattern = re.compile(r'^([a-zA-Z|\ |0-9]){'+ str(min_length) +','+ str(max_length) +'}')
	if not re.match(pattern, field_value):
		return False
	return True
		
