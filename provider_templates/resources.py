from django.conf.urls import url
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization as DjangoAuthorization
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
import models


class AnonymousApiKeyAuthentication(ApiKeyAuthentication):
    def is_authenticated(self, request, **kwargs):
        authorized = super(AnonymousApiKeyAuthentication, self).is_authenticated(request, **kwargs)
        if isinstance(authorized, HttpUnauthorized):
            if request.method == 'GET':
                request.user = AnonymousUser()
                return True
            else:
                return authorized


class TemplateResource(ModelResource):
    group = fields.ToOneField('provider_templates.resources.GroupResource', 'group', full=True)

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
            providers = latest_template.providers.filter(providertemplatedetail_usable=True)
            provider_keys = [p.key for p in providers]
            latest_template_providers = {
                'latest_template': latest_template.name,
                'latest_template_providers': provider_keys
            }
        except models.Template.DoesNotExist:
            latest_template_providers = None

        return self.create_response(request, latest_template_providers)

    def dehydrate(self, bundle):
        template, providers = bundle.obj.latest_template, bundle.obj.latest_template_providers
        bundle.data['latest_template'] = template.name
        bundle.data['latest_template_providers'] = [p.key for p in providers]
        return bundle


class ProviderTemplateDetailResource(ModelResource):
    id = fields.CharField(attribute='concat_id')
    template = fields.ToOneField(TemplateResource, 'template', full=True)
    provider = fields.ToOneField(ProviderResource, 'provider', full=True)

    class Meta:
        queryset = models.ProviderTemplateDetail.objects.all()
        resource_name = 'providertemplate'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'template': ALL_WITH_RELATIONS,
            'provider': ALL_WITH_RELATIONS,
            'usable': ALL,
            'tested': ALL
        }
        excludes = ['concat_id']
        detail_uri_name = 'concat_id'

    def obj_create(self, bundle, **kwargs):
        # Custom obj create to support using concat_id as our fake id/detail_uri_name
        # Catches a uniqueness constraint error and updates the existing object rather than
        # exploding
        parent = super(ProviderTemplateDetailResource, self)
        try:
            return parent.obj_create(bundle, **kwargs)
        except IntegrityError:
            template, provider = bundle.data['template']['name'], bundle.data['provider']['key']
            bundle.obj = models.ProviderTemplateDetail.objects.get(
                template=template, provider=provider)
            return parent.obj_update(bundle, **kwargs)
