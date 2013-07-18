from __future__ import unicode_literals

from lib.frontend import HTTP_METHOD_GET, HTTP_METHOD_POST, \
                         URLS_TYPE_FRENTEND, URLS_TYPE_API, urls
from lib.frontend.views import FeTemplateView

USER_PROJECTS = 'USER_PROJECTS_GET'


class dashboard_view(FeTemplateView):
    '''
    Dashboard view.
    '''
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):

        self.get_api_data('webuser', 'http://localhost:8080/api/siteclient/', \
            'GET', '', 'siteclient_list')
        print self.context

        fe_url = urls.get_format_urls(USER_PROJECTS, URLS_TYPE_FRENTEND, \
                                      username=request.user['username'])
        variables = dict(project_tree_id='project_tree',
                         project_tree_url=fe_url)

        self.context.update(variables)
        return self.render_to_response(self.context)

class project_tree_view(FeTemplateView):

    template_name = 'projects_tree.html'

    def get(self, request, *args, **kwargs):
        api_url = urls.get_format_urls(USER_PROJECTS, URLS_TYPE_API, \
                                       user_id=request.user['user_id'])

        self.get_data(request, api_url, HTTP_METHOD_GET, dict(), 'user_projects')

        return self.render_to_response(self.context)

