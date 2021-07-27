import json

import hunter
from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField, JSONField
from ordered_model.models import OrderedModel

from trace_cockpit.trace_to_json import TraceToJson


class TraceConfig(Model):
    name = CharField(max_length=1024)
    is_active = BooleanField(default=True)

    def do_you_want_to_trace(self, request):
        if not self.is_active:
            return False
        # TODO: Add checks for request.user, URL, ....
        return True

    def trace(self, function, *args, **kwargs):
        trace_to_json = TraceToJson()
        with hunter.trace(trace_to_json):
            ret = function(*args, **kwargs)
        return (
            TraceLog.objects.create(config=self, json=list(trace_to_json.iter_lines_and_close())),
            ret)

class TraceFilter(OrderedModel):
    config = ForeignKey(TraceConfig, on_delete=CASCADE)
    string = CharField(max_length=1024)
    order_with_respect_to = 'config'

class TraceLog(Model):
    config = ForeignKey(TraceConfig, on_delete=CASCADE)
    json = JSONField()