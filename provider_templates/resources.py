from django.db import IntegrityError
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
import models


class TemplateResource(ModelResource):
    group = fields.ToOneField('provider_templates.resources.GroupResource', 'group', full=True)

    class Meta:
        queryset = models.Template.objects.all()
        resource_name = 'template'
        authorization = Authorization()
        filtering = {
            'group': ALL,
            'usable': ALL,
            'datestamp': ALL,
        }

    def dehydrate(self, bundle):
        bundle.data['usable_providers'] = [p.key for p in bundle.obj.usable_providers]
        return bundle


class ProviderResource(ModelResource):
    class Meta:
        queryset = models.Provider.objects.all()
        resource_name = 'provider'
        authorization = Authorization()

    def dehydrate(self, bundle):
        templates = {}
        for group, template in bundle.obj.latest_templates.items():
            if template is not None:
                templates[group.name] = {
                    'latest_template': template.name,
                    'latest_template_providers': [p.key for p in template.usable_providers]
                }
            else:
                templates[group.name] = {
                    'latest_template': None,
                    'latest_template_providers': []
                }
        bundle.data['latest_templates'] = templates
        return bundle


class GroupResource(ModelResource):
    class Meta:
        queryset = models.Group.objects.all()
        resource_name = 'group'
        authorization = Authorization()
        filtering = {
            'stream': ALL
        }

    def dehydrate(self, bundle):
        template, providers = bundle.obj.latest_template, bundle.obj.latest_template_providers
        if template is not None:
            bundle.data['latest_template'] = template.name
            bundle.data['latest_template_providers'] = [p.key for p in providers]
        else:
            bundle.data['latest_template'] = None
            bundle.data['latest_template_providers'] = []
        return bundle


class ProviderTemplateDetailResource(ModelResource):
    id = fields.CharField(attribute='concat_id')
    template = fields.ToOneField(TemplateResource, 'template', full=True)
    provider = fields.ToOneField(ProviderResource, 'provider', full=True)

    class Meta:
        queryset = models.ProviderTemplateDetail.objects.all()
        resource_name = 'providertemplate'
        authorization = Authorization()
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
