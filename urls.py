from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from provider_templates import resources

admin.autodiscover()

api = Api('api')
api.register(resources.TemplateResource())
api.register(resources.ProviderResource())
api.register(resources.GroupResource())

urlpatterns = api.urls + patterns('',
    # Examples:
    # url(r'^$', 'cfme_trackerbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
