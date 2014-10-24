from django.contrib import admin
import models


class BuildAdmin(admin.ModelAdmin):
    list_display = ('number', 'datestamp', 'fails', 'passes', 'skips', 'stream')
admin.site.register(models.Build, BuildAdmin)
