from django.contrib import admin
from ordered_model.admin import OrderedInlineModelAdminMixin, OrderedModelAdmin

from trace_cockpit.models import TraceConfig


class TraceConfigAdmin(OrderedModelAdmin):
    list_display = ['name', 'is_active', 'move_up_down_links']

admin.site.register(TraceConfig, TraceConfigAdmin)
