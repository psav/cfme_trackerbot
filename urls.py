from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from tastypie.api import Api

from provider_templates import resources
from pull_requests import resources as pr_resources

admin.autodiscover()

api = Api('api')
api.register(resources.TemplateResource())
api.register(resources.ProviderResource())
api.register(resources.GroupResource())
api.register(resources.ProviderTemplateDetailResource())
api.register(pr_resources.PRResource())
api.register(pr_resources.RunResource())
api.register(pr_resources.TaskResource())


urlpatterns = patterns('',
    url(r'', include(api.urls)),
    url(r'^templates_to_test$', 'provider_templates.views.templates_to_test'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/doc', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    url('^$', RedirectView.as_view(url=reverse_lazy('tastypie_swagger:index'), permanent=False))
)

if settings.DEBUG:
    urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + urlpatterns
