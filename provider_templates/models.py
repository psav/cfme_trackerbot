from datetime import date

from django.db import models


# The main template class, exposed via the REST API
class Template(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    providers = models.ManyToManyField('Provider', related_name='templates',
        through='ProviderTemplateDetail')
    datestamp = models.DateField(blank=True)
    group = models.ForeignKey('Group', related_name='templates')

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'
        get_latest_by = 'datestamp'
        ordering = ['-datestamp']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # On save, add a date stamp if needed
        if not self.datestamp:
            self.datestamp = date.today()

        # # If a template is marked usable, assume it's been tested
        # if self.usable:
        #     self.tested = True

        return super(Template, self).save(*args, **kwargs)


class Provider(models.Model):
    key = models.CharField(max_length=255, primary_key=True)

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        ordering = ['key']

    def __unicode__(self):
        return self.key


# Template/Provider through model, annotes templates per provider to track
# whether a template has been tested on each provider, and whether or not it's usable
class ProviderTemplateDetail(models.Model):
    template = models.ForeignKey('Template', related_name='providertemplatedetail')
    provider = models.ForeignKey('Provider', related_name='providertemplatedetail')
    usable = models.BooleanField(default=False)
    tested = models.BooleanField(default=False)
    concat_id = models.CharField(max_length=255, editable=False, blank=True)

    class Meta:
        verbose_name = 'Provider/Template Detail'
        verbose_name_plural = 'Provider/Template Details'
        get_latest_by = 'template__datestamp'
        ordering = ['concat_id']
        unique_together = ('template', 'provider')

    def __unicode__(self):
        return '%s on %s' % (self.template.name, self.provider.key)

    def save(self):
        # concatenate the associated names to help tastypie have a friendly URL
        # instead of the auto-int pk
        if self.template and self.provider:
            self.concat_id = '%s_%s' % (self.template.name, self.provider.key)
        return super(ProviderTemplateDetail, self).save()


# Template grouping, normally used for stream name,
# but can be handy for things like power control
class Group(models.Model):
    name = models.CharField(max_length=63, primary_key=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def latest_template(self):
        # For a given group, list the latest usable template
        return Template.objects.filter(providertemplatedetail__usable=True, group=self).latest()

    @property
    def latest_template_providers(self):
        # For a given group, list the latest usable template
        return self.latest_template.providers.filter(providertemplatedetail__usable=True)
