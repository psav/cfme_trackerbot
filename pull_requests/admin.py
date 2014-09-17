from django.contrib import admin
import models


class PRAdmin(admin.ModelAdmin):
    list_display = ('number', 'description', 'current_commit_head', 'wip', 'status')
admin.site.register(models.PR, PRAdmin)


class RunAdmin(admin.ModelAdmin):
    list_display = ('pr', 'commit', 'datestamp', 'status')
admin.site.register(models.Run, RunAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('tid', 'run', 'datestamp', 'result', 'stream', 'provider', 'template',
                    'vm_name', 'cleanup')
admin.site.register(models.Task, TaskAdmin)
