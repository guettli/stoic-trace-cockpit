from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin

from trace_cockpit.html import jsontrace_to_html
from trace_cockpit.htmlutils import count_dict_to_html
from trace_cockpit.models import TraceConfig, TraceLog


class TraceConfigAdmin(OrderedModelAdmin):
    list_display = ['name', 'is_active', 'move_up_down_links']
    readonly_fields = ['hint', 'link_to_logs']

    def hint(self, config: TraceConfig):
        if not config.is_active:
            return format_html('<div style="color: red">Config is not active. No logs will be created')
        first = TraceConfig.objects.filter(is_active=True).order_by('order').first()
        if first and first != config:
            return format_html('''
             <div style="color: red">Config "{first}" is active and has a higher order. The above config will only
             be called if the higher config does not match to the request.</div>''', first=first)
        return 'Everything looks fine'

    def link_to_logs(self, config: TraceConfig):
        if not config.id:
            return ''
        count = TraceLog.objects.filter(config=config).count()
        if not count:
            return 'There are no logs for this config yet'
        return format_html('<a href="{}?config__id__exact={}">{} {} Logs</a>',
                           reverse('admin:trace_cockpit_tracelog_changelist'), config.id, count,
                           config.name)


admin.site.register(TraceConfig, TraceConfigAdmin)


class TraceLogAdmin(ModelAdmin):
    list_display = ['config', 'datetime_created', 'http_method', 'url', 'http_status', 'log_size']
    readonly_fields = ['config', 'success', 'html', 'error_message', 'url', 'http_status', 'http_method',
                       'skipped_events_because_max_reached_html',
                       'skipped_modules_html',
                       ]

    list_filter = (
        'config',
        'datetime_created',
        'success')

    def html(self, log):
        return jsontrace_to_html(log.json_lines.splitlines())

    def skipped_modules_html(self, log: TraceLog):
        return count_dict_to_html(log.skipped_modules)

    skipped_modules_html.short_description = 'Skipped modules'

    def skipped_events_because_max_reached_html(self, log: TraceLog):
        return count_dict_to_html(log.skipped_events_because_max_reached)

    skipped_events_because_max_reached_html.short_description = 'Skipped events, because max reached'


    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(TraceLog, TraceLogAdmin)
