
from __future__ import unicode_literals
from lib.frontendlib import FeTemplateView

class dashboard_view(FeTemplateView):
    '''
    Dashboard view.
    '''
    template_name = 'dashboard.html'
    
    def get(self, request, *args, **kwargs):

        #self.get_api_data('webuser', 'http://localhost:8080/api/siteclient/', \
        #    'GET', '', 'siteclient_list')
        #print self.context
        return self.render_to_response(self.context)