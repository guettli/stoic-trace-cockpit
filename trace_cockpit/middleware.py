from trace_cockpit.models import TraceConfig


class TraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for config in TraceConfig.objects.filter(is_active=True):
            if not config.do_you_want_to_trace(request):
                continue
