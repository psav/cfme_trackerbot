from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
import models


class PRResource(ModelResource):
    runs = fields.ToManyField('pull_requests.resources.RunResource',
                              'run_set', null=True, blank=True)
    status = fields.CharField(attribute='status', readonly=True)

    class Meta:
        queryset = models.PR.objects.all()
        resource_name = 'pr'
        authorization = Authorization()
        filtering = {'number': ALL}

    def dehydrate(self, bundle):
        bundle.data['runs'] = [{'id': p.id,
                                'result': p.status,
                                'commit': p.commit} for p in
                               bundle.obj.run_set.all().order_by('-datestamp')]
        return bundle


class RunResource(ModelResource):
    #pr = fields.ForeignKey(PRResource, 'pr')
    pr = fields.ToOneField(PRResource, 'pr')
    tasks = fields.ToManyField('pull_requests.resources.TaskResource',
                               'task_set', null=True, blank=True)
    status = fields.CharField(attribute='status', readonly=True)

    class Meta:
        queryset = models.Run.objects.all()
        resource_name = 'run'
        authorization = Authorization()
        filtering = {'retest': ALL, 'pr': ALL_WITH_RELATIONS}
        ordering = ['datestamp']

    def dehydrate(self, bundle):
        bundle.data['tasks'] = [{'tid': p.tid,
                                 'template': p.template,
                                 'result': p.result} for p in bundle.obj.task_set.all()]
        return bundle


class TaskResource(ModelResource):
    #run = fields.ForeignKey(RunResource, 'run')
    run = fields.ToOneField(RunResource, 'run', null=True, blank=True)

    class Meta:
        queryset = models.Task.objects.all()
        resource_name = 'task'
        authorization = Authorization()
        filtering = {'result': ALL, 'cleanup': ALL}

    def dehydrate(self, bundle):
        bundle.data['pr_number'] = bundle.obj.run.pr.number

        return bundle
