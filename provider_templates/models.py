from datetime import date

from django.db import models


# The main template class, exposed via the REST API
class Template(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    providers = models.ManyToManyField('Provider', related_name='templates')
    usable = models.BooleanField(default=True)
    datestamp = models.DateField(blank=True)
    group = models.ForeignKey('Group', related_name='templates')

    class Meta:
        verbose_name = ('Template')
        verbose_name_plural = ('Templates')
        get_latest_by = 'datestamp'
        ordering = ['-datestamp']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """On save, add a date stamp if needed"""
        if not self.datestamp:
            self.datestamp = date.today()
        return super(Template, self).save(*args, **kwargs)


class Provider(models.Model):
    key = models.CharField(max_length=255, primary_key=True)

    class Meta:
        verbose_name = ('Provider')
        verbose_name_plural = ('Providers')
        ordering = ['key']

    def __unicode__(self):
        return self.key


# Template grouping, normally used for stream name,
# but can be handy for things like power control
class Group(models.Model):
    name = models.CharField(max_length=63, primary_key=True)

    class Meta:
        verbose_name = ('Group')
        verbose_name_plural = ('Groups')
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def latest_template(self):
        # For a given group, list the latest usable template that has providers associated with it
        return self.templates.exclude(providers=None).filter(usable=True).latest()
