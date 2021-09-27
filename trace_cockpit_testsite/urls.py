from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, reverse
from django.utils.html import format_html


def dummy_view(request):
    i = 0
    i += 1
    return HttpResponse(f'<html><body>i: {i}</body></html>')

def start_page(request):
    return HttpResponse(format_html('''
    <html>
     <h1>Stoic Trace Cockpit</h1>
     Thank you for choosing stoic trace cockpit!
     
     <p>
      Configuring the trace cockpit gets done via the <a href="{link_to_admin}">Admin</a>.
     </p>
     
     <p>
      I like feedback! Is there something which is not working? What could be improved?
      Please provide your feedback via the 
      <a href="https://github.com/guettli/stoic-trace-cockpit/issues">Github Issue Tracker</a>.
    </p>''', link_to_admin=reverse('admin:app_list', args=('trace_cockpit',))))
     
     
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dummy_view', dummy_view, name='dummy_view'),
    path('', start_page, name='start_page'),
]
