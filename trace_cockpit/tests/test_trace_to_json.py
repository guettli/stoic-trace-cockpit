import hunter

from trace_cockpit.testutils import norm_json_event_list
from trace_cockpit.trace_to_json import TraceToJson
from trace_cockpit_testsite.utils import dummy_get_response


def test_trace_to_json(rf):
    trace_to_json = TraceToJson()
    with hunter.trace(trace_to_json):
        dummy_get_response(rf.get('/'))
    expected = norm_json_event_list(trace_to_json.iter_lines_and_close())
    assert expected == [{'filename': 'utils.py',
                         'function': 'dummy_get_response',
                         'kind': 'call',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': 'def dummy_get_response(request):'},
                        {'filename': 'utils.py',
                         'function': 'dummy_get_response',
                         'kind': 'line',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': '    i = 0'},
                        {'filename': 'utils.py',
                         'function': 'dummy_get_response',
                         'kind': 'line',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': '    i += 1'},
                        {'filename': 'utils.py',
                         'function': 'dummy_get_response',
                         'kind': 'line',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': "    return HttpResponse('<html><body>{i}</body></html>')"},
                        {'filename': 'utils.py',
                         'function': 'dummy_get_response',
                         'kind': 'return',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': "    return HttpResponse('<html><body>{i}</body></html>')"}]
