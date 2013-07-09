
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
        variables = dict(project_tree_id='project_tree', 
                         project_tree_url='/secure/testaccount/projects/')
        self.context.update(variables)
        
        return self.render_to_response(self.context)

class project_tree_view(FeTemplateView):
    
    template_name = 'projects_tree.html'

    def get(self, request, *args, **kwargs):        
        if 'username' in kwargs:
            self.get_api_data(kwargs['username'], 'http://localhost:8080/api/projects/1/', \
	            			  'GET', '', 'user_projects')
        
        return self.render_to_response(self.context)