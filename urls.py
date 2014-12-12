from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from tastypie.api import Api

from provider_templates import resources
from pull_requests import resources as pr_resources
from grapher import resources as grapher_resources
from pull_requests import views
from grapher import views as grapher_views
from utils import utils as util_views

admin.autodiscover()

api = Api('api')
api.register(resources.TemplateResource())
api.register(resources.ProviderResource())
api.register(resources.GroupResource())
api.register(resources.ProviderTemplateDetailResource())
api.register(pr_resources.PRResource())
api.register(pr_resources.RunResource())
api.register(pr_resources.TaskResource())
api.register(grapher_resources.BuildResource())


urlpatterns = patterns('',
    # includes
    url(r'', include(api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^template/', include('provider_templates.urls')),
    url(r'^api/doc', include('tastypie_swagger.urls', namespace='tastypie_swagger')),

    # endpoints
    url('^$', RedirectView.as_view(url=reverse_lazy('tastypie_swagger:index'), permanent=False)),
    url(r'^prs$', views.index),
    url(r'^pr/(?P<pr_number>\d+)$', views.pr_detail),
    url(r'^run/(?P<run_number>\d+)$', views.run_detail),
    url(r'^retest/(?P<pr_number>\d+)$', views.retest),
    url(r'^graph/(?P<stream_name>.*)$', grapher_views.show_graph),
    url(r'^sauce_proxy/(?P<sauce_url>.*)$', util_views.sauce_proxy),
)

if settings.DEBUG:
    urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + urlpatterns
