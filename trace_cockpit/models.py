import json

import hunter
from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField, JSONField, TextField
from ordered_model.models import OrderedModel

from trace_cockpit.trace_to_json import TraceToJson


class TraceConfig(OrderedModel):
    name = CharField(max_length=1024)
    is_active = BooleanField(default=True)
    trace_request_eval = CharField(max_length=1024, default='',
                                   help_text='''Trace a request, if the expression matches.
                                   Example: "request.user.username=='foo'"
                                   If empty, then every request gets traced''')

    def do_you_want_to_trace(self, request):
        if not self.is_active:
            return False
        if not self.trace_request_eval:
            return True
        try:
            return eval(self.trace_request_eval)
        except Exception as exc:
            TraceLog.objects.create(success=False, error_message=f'Eval failed: {exc}',
                                    config=self)
            return False

    def trace(self, function, *args, **kwargs):
        trace_to_json = TraceToJson()
        with hunter.trace(trace_to_json):
            ret = function(*args, **kwargs)
        return (
            TraceLog.objects.create(config=self, json=list(trace_to_json.iter_lines_and_close())),
            ret)


class TraceLog(Model):
    config = ForeignKey(TraceConfig, on_delete=CASCADE)
    json = JSONField(default=[])
    success = BooleanField(default=True)
    error_message = TextField(default='')
