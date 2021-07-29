import hunter

from trace_cockpit.html import jsontrace_to_html
from trace_cockpit.models import TraceLog
from trace_cockpit.trace_to_json import TraceToJson
from trace_cockpit_testsite.utils import dummy_get_response


def test_jsontrace_to_html(rf):
    trace_to_json = TraceToJson()
    with hunter.trace(trace_to_json):
        dummy_get_response(rf.get('/'))
    html = jsontrace_to_html(trace_to_json.iter_lines_and_close())
    assert 'return HttpResponse(&#x27;&lt;html&gt;' in html
