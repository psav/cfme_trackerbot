from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.fields import ForeignKey
from provider_templates.resources import GroupResource
import models


class BuildResource(ModelResource):
    stream = ForeignKey(GroupResource, 'stream')

    class Meta:
        queryset = models.Build.objects.all()
        resource_name = 'build'
        authorization = Authorization()
        filtering = {'stream': ALL_WITH_RELATIONS}
        ordering = ['datestamp']
