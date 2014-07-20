from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
import models


class ProviderTemplatesForm(forms.ModelForm):
    templates = forms.ModelMultipleChoiceField(
        queryset=models.Template.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=('Templates'),
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(ProviderTemplatesForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['templates'].initial = self.instance.templates.all()

    class Meta:
        model = models.Provider

    def save(self, commit=True):
        provider = super(ProviderTemplatesForm, self).save(commit=False)

        if commit:
            provider.save()

        if provider.pk:
            provider.templates.clear()
            provider.templates = self.cleaned_data['templates']
            self.save_m2m()

        return provider


class GroupTemplatesInline(admin.StackedInline):
    model = models.Template


class ProviderAdmin(admin.ModelAdmin):
    form = ProviderTemplatesForm


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'latest_template')
    inlines = [GroupTemplatesInline]

    def latest_template(self, obj):
        return '%s: %s' % (
            obj.latest_template,
            ', '.join(p.key for p in obj.latest_template.providers.all())
        )


admin.site.register(models.Template)
admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.Group, GroupAdmin)
