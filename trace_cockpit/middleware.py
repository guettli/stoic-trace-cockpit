from contextlib import ExitStack

from trace_cockpit.models import TraceConfig


class TraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        trace_configs_for_this_request = []
        for config in TraceConfig.objects.filter(is_active=True):
            if not config.do_you_want_to_trace(request):
                continue
            trace_configs_for_this_request.append(config)
        if not trace_configs_for_this_request:
            return self.get_response(request)
        #get_response = lambda: (None, self.get_response(request))
        #for config in trace_configs_for_this_request:
        #    get_response = lambda: config.trace(get_response)
        #get_response = lambda: config.trace(get_response)
        return config.trace(self.get_response, request)[1]
