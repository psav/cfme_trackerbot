from django.contrib import admin
import models


class ProviderTemplateDetailAdmin(admin.ModelAdmin):
    list_filter = ('tested', 'usable')


class GroupAdmin(admin.ModelAdmin):
    list_filter = ('active', 'stream')

    def get_queryset(self, request):
        # copied from django default impl, except qs explicitly uses the
        # '_unfiltered_objects' manager instead of 'objects' to include inactive groups
        qs = self.model._unfiltered_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

admin.site.register(models.Template)
admin.site.register(models.ProviderTemplateDetail, ProviderTemplateDetailAdmin)
admin.site.register(models.Provider)
admin.site.register(models.Group, GroupAdmin)
