from django.http import HttpResponse


def dummy_get_response(request):
    i = 0
    i += 1
    return HttpResponse('<html><body>{i}</body></html>')