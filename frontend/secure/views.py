from django.http import HttpResponse
# from django.views.base import TemplateView
from django.core import serializers
from lib.frontendlib import hmac_auth, FeTemplateView
from django.template.loader import render_to_string
class dashboard_view(FeTemplateView):
    '''
    Dashboard view.
    '''

    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):

        self.get_api_data('webuser', 'http://localhost:8080/api/siteclient/', \
            'GET', '', 'siteclient_list')
        return self.render_to_response(self.context)