from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from provider_templates import resources

admin.autodiscover()

api = Api('api')
api.register(resources.TemplateResource())
api.register(resources.ProviderResource())
api.register(resources.GroupResource())
api.register(resources.ProviderTemplateDetailResource())

urlpatterns = api.urls + patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
