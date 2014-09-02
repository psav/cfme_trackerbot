from django.contrib import admin
import models


class ProviderTemplateDetailAdmin(admin.ModelAdmin):
    list_filter = ('tested', 'usable')

admin.site.register(models.Template)
admin.site.register(models.ProviderTemplateDetail, ProviderTemplateDetailAdmin)
admin.site.register(models.Provider)
admin.site.register(models.Group)
