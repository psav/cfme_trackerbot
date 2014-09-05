from django.db import models
#from provider_templates.models import Template


# Create your models here.
class PR(models.Model):
    number = models.IntegerField()
    description = models.TextField()
    current_commit_head = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __unicode__(self):
        return "{}: {}".format(str(self.number), self.state)


class Run(models.Model):
    pr = models.ForeignKey('PR', related_name='run_set')
    result = models.CharField(max_length=255)
    commit = models.CharField(max_length=255, default="None")
    datestamp = models.DateTimeField()

    def __unicode__(self):
        return "{}: {} ({})".format(str(self.pr), self.result, self.datestamp)


class Task(models.Model):
    run = models.ForeignKey('Run', related_name='task_set')
    output = models.TextField()
    result = models.CharField(max_length=255)
    template = models.CharField(max_length=255, default="None")

    def __unicode__(self):
        return "{}: {}".format(int(self.run.pr.number), self.template)
