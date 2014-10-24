from django.db import models
#from provider_templates.models import Template


# Create your models here.
class Build(models.Model):
    number = models.IntegerField()
    stream = stream = models.ForeignKey('provider_templates.Group',
                                        limit_choices_to={'stream': True})
    datestamp = models.DateTimeField()
    passes = models.IntegerField()
    fails = models.IntegerField()
    skips = models.IntegerField()

    def __unicode__(self):
        return "{}".format(str(self.number))
