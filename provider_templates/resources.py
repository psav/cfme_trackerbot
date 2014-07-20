from django.conf.urls import url
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL
from tastypie.utils import trailing_slash
import models


class ProviderResource(ModelResource):
    class Meta:
        queryset = models.Provider.objects.all()
        resource_name = 'provider'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()


class GroupResource(ModelResource):
    class Meta:
        queryset = models.Group.objects.all()
        resource_name = 'group'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

    def prepend_urls(self):
        return [
            self._build_url('latest_template')
        ]

    def _build_url(self, property_name):
        return url(
            "%s/(?P<name>\w[\w/-]+)/%s%s$" % (
                self._meta.resource_name, property_name, trailing_slash()),
            self.wrap_view('get_%s' % property_name),
            name="api_%s_%s" % (self._meta.resource_name, property_name)
        )

    def _obj(self, request, **kwargs):
        bundle = self.build_bundle(data={'name': kwargs['name']}, request=request)
        return self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))

    def get_latest_template(self, request, **kwargs):
        try:
            latest_template = self._obj(request, **kwargs).latest_template
            providers = [p.key for p in latest_template.providers.all()]
            latest_template_providers = {
                'latest_template': latest_template.name,
                'latest_template_providers': providers
            }
        except models.Template.DoesNotExist:
            latest_template_providers = None

        return self.create_response(request, latest_template_providers)


class TemplateResource(ModelResource):
    class Meta:
        queryset = models.Template.objects.all()
        resource_name = 'template'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'group': ALL,
            'usable': ALL,
            'datestamp': ALL,
        }

    # dehydrate: turn provider and group objects into strings
    def dehydrate(self, bundle):
        bundle.data['group'] = bundle.obj.group.name
        bundle.data['providers'] = [provider.key for provider in bundle.obj.providers.all()]
        return super(TemplateResource, self).dehydrate(bundle)

    # hydrate: turn provider and group strings into objects, creating providers if needed
    def hydrate(self, bundle):
        try:
            bundle.obj = models.Template.objects.get(name=bundle.data['name'])
        except models.Template.DoesNotExist:
            bundle.obj = models.Template(name=bundle.data['name'],
                datestamp=bundle.data['datestamp'])
        bundle.obj.group = models.Group.objects.get(name=bundle.data['group'])
        providers = []
        for provider_key in bundle.data['providers']:
            # Will create provider keys that don't exist
            provider, __ = models.Provider.objects.get_or_create(key=provider_key)
            providers.append(provider)
        bundle.obj.providers = providers
        return super(TemplateResource, self).hydrate(bundle)
