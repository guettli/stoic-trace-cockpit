import json

import hunter
from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField, JSONField, TextField, DateTimeField, \
    URLField, PositiveIntegerField
from django.http import HttpRequest, HttpResponse
from ordered_model.models import OrderedModel

from trace_cockpit.trace_to_json import TraceToJson


class TraceConfig(OrderedModel):
    name = CharField(max_length=1024)
    is_active = BooleanField(default=True)
    trace_request_eval = CharField(max_length=1024, default='',
                                   help_text='''Trace a request, if the expression matches.
                                   Example: "request.user.username=='foo'"
                                   If empty, then every request gets traced.
                                   For convenience request.get_full_path() is available in the variable "url".
                                   Example2: "'fooo' in url"
                                   Nested expressions are possible. 
                                   Example3: "request.user.username=='foo' and ('bar' in url or url.startswith('/blue'))"
                                   
                                   This flexiblity has a draw-back. An evil staff-user could do "from foo.models import MyModel; MyModel.objects.all().delete()" or other fancy evil things.''',
                                   blank=True)

    max_event_count_per_module = PositiveIntegerField(default=TraceToJson.max_event_count_per_module)

    def __str__(self):
        return self.name

    def do_you_want_to_trace(self, request: HttpRequest):
        url = request.get_full_path_info() # no-qa: Needed for eval()
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

    def trace_get_response(self, get_response, request):
        trace_to_json = TraceToJson(max_event_count_per_module=self.max_event_count_per_module)
        with hunter.trace(trace_to_json):
            response = get_response(request)
        return (
            TraceLog.objects.create(config=self, json_lines=''.join(trace_to_json.iter_lines_and_close()),
                                    http_status=f'{response.status_code}: {response.reason_phrase}',
                                    http_method=request.method,
                                    url=request.get_full_path_info(),
                                    skipped_modules=trace_to_json.skipped_modules,
                                    skipped_events_because_max_reached=trace_to_json.skipped_events_because_max_reached,

                                    ),
            response)


class TraceLog(Model):
    config = ForeignKey(TraceConfig, on_delete=CASCADE)
    datetime_created = DateTimeField(auto_now_add=True)
    json_lines = TextField(default='', editable=False)
    success = BooleanField(default=True)
    error_message = TextField(default='')
    url = URLField(default='')
    http_status = CharField(max_length=1024, default='')
    http_method = CharField(max_length=1024, default='')
    skipped_modules = JSONField(default=dict, blank=True, editable=False)
    skipped_events_because_max_reached = JSONField(default=dict, blank=True, editable=False)

    @property
    def log_size(self):
        return len(self.json_lines)
