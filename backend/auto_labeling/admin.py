from django.contrib import admin

from .models import AutoLabelingConfig


class AutoLabelingConfigAdmin(admin.ModelAdmin):
    list_display = ('project', 'model_name', 'model_attrs',)
    ordering = ('project',)

    def get_readonly_fields(self, request, obj=None):
        return ["model_name"] if obj else []


admin.site.register(AutoLabelingConfig, AutoLabelingConfigAdmin)
