from django.http import HttpResponse
from django.views import generic
import urllib2
from rest_framework.parsers import JSONParser

class user_view(generic.ListView):
    template_name = 'userlist.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        gh_url = 'http://localhost:8080/api/siteclient/'
        req = urllib2.Request(gh_url)
        handler = urllib2.urlopen(req)
        #stream = StringIO.StringIO(handler.getcode())
        data = JSONParser().parse(handler)
        return data
