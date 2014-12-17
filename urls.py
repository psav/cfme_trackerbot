from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api

from provider_templates import resources
from pull_requests import resources as pr_resources
from grapher import resources as grapher_resources

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
    # TODO: Break the API up by app, similar to the URLs
    url(r'', include(api.urls)),
    url(r'', include("dashboard.urls")),
    url(r'^pr/?$', include("pull_requests.urls")),
    url(r'^template/', include("provider_templates.urls")),
    url(r'^graph/', include("grapher.urls")),
    url(r'^api/doc', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + urlpatterns
