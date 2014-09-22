from django.db import models
#from provider_templates.models import Template


# Create your models here.
class PR(models.Model):
    number = models.IntegerField(primary_key=True)
    description = models.TextField()
    current_commit_head = models.CharField(max_length=255)
    wip = models.BooleanField(default=False)

    @property
    def status(self):
        runs = self.run_set.all().order_by('-datestamp')
        if runs:
            return runs[0].status
        else:
            return "untested"

    def __unicode__(self):
        return "{}: {}".format(str(self.number), self.status)


class Run(models.Model):
    pr = models.ForeignKey('PR', related_name='run_set')
    commit = models.CharField(max_length=255, default="None")
    datestamp = models.DateTimeField()

    @property
    def status(self):
        tasks = self.task_set.all()
        results = []
        for task in tasks:
            results.append(task.result)
        if "invalid" in results and len(results) > 0:
            return "invalid"
        elif ("pending" in results or "provisioning" in results
              or "running" in results) and len(results) > 0:
            return "pending"
        elif len(results) > 0:
            all_passed = all([result == "passed" for result in results])
            if all_passed:
                return "passed"
            else:
                return "failed ({}/{})".format(results.count("failed"), len(results))

    def __unicode__(self):
        return "{}: {} ({})".format(str(self.pr), self.status, self.datestamp)


class Task(models.Model):
    tid = models.CharField(primary_key=True, max_length=16)
    run = models.ForeignKey('Run', related_name='task_set', null=True)
    datestamp = models.DateTimeField()
    output = models.TextField()
    result = models.CharField(max_length=255)
    stream = models.CharField(max_length=255, default="None")
    template = models.CharField(max_length=255, default="None")
    provider = models.CharField(max_length=255, default="None")
    vm_name = models.CharField(max_length=255, default="None")
    cleanup = models.BooleanField(default=False)

    def __unicode__(self):
        return "{}: {} ({})".format(int(self.run.pr.number), self.stream, self.result)
