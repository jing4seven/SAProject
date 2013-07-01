from django.http import HttpResponse
from django.views import generic
from django.core import serializers
from lib.frontendlib import hmac_auth
import requests

class user_view(generic.ListView):
    template_name = 'userlist.html'
    context_object_name = 'user_list'

    # api_request = lib.frontendlib.get_api_request('none')
    # api_request = requests.Session()

    # api_request.auth = hmac_auth('none')
    # rep = api_request.get('http://localhost:8080/api/siteclient/')
    # req = requests.get('http://localhost:8080/api/siteclient/', auth=hmac_auth('kenneth'))
    # gh_url = 'http://localhost:8080/api/siteclient/'
    # req = urllib2.Request(gh_url)
    # handler = urllib2.urlopen(req)
    # queryset = serializers.deserialize('json', req.text)
    # def get_queryset(self):

    #     return queryset    
    #     # req.add_header('AUTHORIZATION', 'ApiKey username:signature')
    #     # req.add_header('X_SAPROJECT_CLIENT_ID', 'rqEWEQOx3m1XlXyJ4VgzdRehci01a3pWx4G8AnNP0UI')
       
    #     #stream = StringIO.StringIO(handler.getcode())
    #     # data = JSONParser().parse(handler)
         
    #     return data
