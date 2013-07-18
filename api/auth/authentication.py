import hmac
import re
import hashlib
import string
from rest_framework import authentication, exceptions
from api.auth.models import site_client as site_client_model
from api.secure.models import user

class api_auth(authentication.BaseAuthentication):
    '''
    Authentication for api.

    Use HMAC for authentication.

    Available auth header format:
    HTTP_AUTHORIZATION: ApiKey [username]:[signature]

    or

    HTTP_AUTHORIZATION: ApiKey none:[signature]
    X_SAPROJECT_CLIENT_ID: [client_id]

    Ps: 'X_SAPROJECT_CLIENT_ID' can be setted in django settings.
    '''
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request)

        if len(string.strip(auth_header)) == 0:
            raise exceptions.NotAuthenticated()

        auth_matcher = re.match(r'^ApiKey ([a-zA-Z|0-9|\_]+):([a-zA-Z|0-9]+)$', auth_header)

        if not auth_matcher:
            raise exceptions.AuthenticationFailed()

        username = auth_matcher.group(1)

        try:
            if username == 'none':
                client_id = self._get_client_id(request)
            else:
                client_id = user.objects.get(username=username).site_client.client_id

            security_key = site_client_model.objects.get(client_id=client_id).security_key
        except:
            raise exceptions.PermissionDenied()

        if security_key is None:
            raise exceptions.PermissionDenied()

        signature = auth_matcher.group(2)

        uri = '%s://%s%s' % ('https' if request.is_secure() else 'http',
                                         request.get_host(), request.path)

        hmac_message = '{method}{full_path}{body}'.format(
            method=request.method.upper(),
            full_path=uri,
            body= request.body or '',
        )

        hmac_key = hmac.new(str(security_key), str(hmac_message), hashlib.sha1)

        if str(hmac_key.hexdigest()) != signature:
            raise exceptions.AuthenticationFailed("Signature error!")

        if username == 'none':
            username = None

        return (username, None)

    def authenticate_header(self, request):
        return None

    def _get_client_id(self, request):
        '''
        Get client_id in header.
        '''
        client_id =  request.META.get('HTTP_X_SAPROJECT_CLIENT_ID', None)

        if client_id is None:
            raise exceptions.NotAuthenticated('Please provide X_SAPROJECT_CLIENT_ID header in your request.')

        client_id_matcher = re.match(r'^[a-zA-Z|0-9]+$', client_id)

        if not client_id_matcher:
            raise exceptions.AuthenticationFailed()

        return client_id_matcher.group(0)
