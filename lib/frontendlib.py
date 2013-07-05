import hashlib
import hmac
from django.conf import settings
from django.template import Context
from django.views.generic.base import TemplateView
import requests # http://www.python-requests.org
from requests.auth import AuthBase
from requests.sessions import Session
from lib.wrapper import singleton

class hmac_auth(AuthBase):
	'''
	HMAC Authentication class for api request.

	Caculate signature for each request between frontend and api.
	'''
	def __init__(self, username, url, method, data):
		self.username = username
		self.url = url
		self.method = method
		self.data = data

	def __call__(self, r):
		'''
		Prepare hmac auth header.

		We add client id into request header only if username is none.
		'''
		if not self.username or self.username == 'none':
			username = 'none'
			client_id_param = settings.FRONT_END['HEAD_CLIENT_ID']
			client_id = settings.FRONT_END['CLIENT_ID']
			r.headers[client_id_param] = client_id 	
		hmac_message = '{method}{full_path}{body}'.format(
			method=self.method.upper(),
			full_path= self.url,
			body=  self.data or '',
		)
		security_key = settings.FRONT_END['CLIENT_SECURITY_KEY']
		signature = hmac.new(security_key, hmac_message, hashlib.sha1).hexdigest() 
		r.headers['AUTHORIZATION'] = 'ApiKey %s:%s' % (self.username, signature)

		return r


class FeTemplateView(TemplateView):
	'''
	A view with more convience request data from api.
	'''

	req_session = None
	context_data = {} # data use for context
	context = None

	@singleton
	class api_request_session(Session):
		pass

	def __init__(self, *args, **kwargs):
		self.req_session = self.api_request_session()
		self.context = self.__get_default_context__()

	def get_api_data(self, username, url, method, data, obj_name):
		self.req_session.auth = hmac_auth('none', url, method, data)

		resp = self.req_session.get(url)
		
		if resp.status_code == requests.codes.ok:			
			self.context_data[obj_name] = resp.json()		
			self.context.update(self.context_data)						
				
				
	def __get_default_context__(self):
		default_context_data = Context()
		default_context_data['ENVIRONMENT'] = settings.FRONT_END['ENVIRONMENT']
		return default_context_data
				
				
				