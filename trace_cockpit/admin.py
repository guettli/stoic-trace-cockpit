from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from trace_cockpit.models import TraceConfig, TraceFilter


class FilterInline(OrderedTabularInline):
    model = TraceFilter
    extra = 1
    ordering = ('order',)
    fields = ('string', 'move_up_down_links',)
    readonly_fields = ('move_up_down_links',)

class TraceConfigAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'is_active']
    inlines = [FilterInline]

admin.site.register(TraceConfig, TraceConfigAdmin)
