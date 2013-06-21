import random
import hashlib
import base64

def gen_random_key():
	'''
	Generate a hash key.
	'''
	random_str = str(random.getrandbits(256))
	key = base64.b64encode(hashlib.sha256(random_str).digest(), random.choice(generate_radom_list())).rstrip('==')
	return key

def gen_random_key_by_given_key(g_key):
	'''
	Generate a hash key by a given key.
	'''
	if not g_key or len(g_key) == 0:
		return None

	security_key = base64.b64encode(g_key, random.choice(generate_radom_list())).rstrip('==')
	return security_key

def generate_radom_list(length=2, count=6):
	'''
	Generate a random list by condition.

	condition: length=2, count=6
	return:
	['aE', 'bc', '5w', 'wc', 'ew', 'ac']
	'''
	basic_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	arr = []
	i=0
	while i<count:	
		word = ''
		j=0
		while j < length:
			word += random.choice(basic_str)
			j=j+1
		arr.append(word)
		i=i+1

	return arr