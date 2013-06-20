import hmac
import re
import hashlib
import string
from rest_framework import authentication, exceptions
from api.auth.models import auth_hmac

class api_auth(authentication.BaseAuthentication):
	'''
	Authentication for api.

	Use HMAC for authentication.
	'''
	def authenticate(self, request):
		auth_header = authentication.get_authorization_header(request)

		if len(string.strip(auth_header)) == 0:
			raise exceptions.NotAuthenticated()

		auth_matcher = re.match(r'^ApiKey (.*?):(.*?)$', auth_header)

		if not auth_matcher:
			raise exceptions.AuthenticationFailed()

		client_id = auth_matcher.group(0)

		try:
			security_key = auth_hmac.objects.get(client_id=client_id)
		except:
			raise exceptions.PermissionDenied()

		signature = auth_matcher.group(1)

		hmac_message = '{method}{full_path}{body}'.format(
			method=request.method.upper(),
			full_path=request.path_url,
			body=request.data or '',
		)

		hmac_key = hmac.new(security_key, hmac_message, hashlib.sha1)

		if not hmac_key.hexdigest() == signature:
			raise exceptions.AuthenticationFailed("Signature error!")

		return (auth_header, None)

	def authenticate_header(self, request):
		return None