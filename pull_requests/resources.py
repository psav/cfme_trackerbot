from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
import models


class PRResource(ModelResource):

    class Meta:
        queryset = models.PR.objects.all()
        resource_name = 'pr'
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['runs'] = [{'id': p.id,
                                'result': p.result} for p in bundle.obj.run_set.all()]
        return bundle


class RunResource(ModelResource):

    class Meta:
        queryset = models.Run.objects.all()
        resource_name = 'run'
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['tasks'] = [{'id': p.id,
                                'template': p.template,
                                'result': p.result} for p in bundle.obj.task_set.all()]
        return bundle


class TaskResource(ModelResource):

    class Meta:
        queryset = models.Task.objects.all()
        resource_name = 'task'
        authorization = Authorization()

