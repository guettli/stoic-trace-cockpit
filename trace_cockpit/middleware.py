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
        #config1, config2 = trace_configs_for_this_request
        #return config2.trace(config1.trace, self.get_response, request)[1][1]
        handler = lambda: (None, self.get_response(request))
        for config in trace_configs_for_this_request:
            handler = self.handler(config.trace, handler)
        return handler()[1]

    def handler(self, method, handler):
        return lambda: method(handler)[1]

