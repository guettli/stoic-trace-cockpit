from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from ordered_model.admin import OrderedInlineModelAdminMixin, OrderedModelAdmin

from trace_cockpit.html import jsontrace_to_html
from trace_cockpit.models import TraceConfig, TraceLog


class TraceConfigAdmin(OrderedModelAdmin):
    list_display = ['name', 'is_active', 'move_up_down_links']
    readonly_fields = ['hint']

    def hint(self, config: TraceConfig):
        if not config.is_active:
            return format_html('<div style="color: red">Config is not active. No logs will be created')
        first = TraceConfig.objects.filter(is_active=True).order_by('order').first()
        if first and first != config:
            return format_html('''
             <div style="color: red">Config "{first}" is active and has a higher order. The above config will only
             be called if the higher config does not match to the request.</div>''', first=first)
        return ''
admin.site.register(TraceConfig, TraceConfigAdmin)

class TraceLogAdmin(ModelAdmin):
    list_display = ['config', 'datetime_created', 'http_status', 'log_size']
    readonly_fields = ['config', 'success', 'html', 'error_message', 'url', 'http_status']

    def html(self, log):
        return jsontrace_to_html(log.json)

admin.site.register(TraceLog, TraceLogAdmin)
