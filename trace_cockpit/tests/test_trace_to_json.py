import hunter

from trace_cockpit.testutils import norm_json_event_list
from trace_cockpit.trace_to_json import TraceToJson
from trace_cockpit_testsite.utils import dummy_foo


def test_trace_to_json():
    trace_to_json = TraceToJson()
    with hunter.trace(trace_to_json):
        dummy_foo()
    expected = norm_json_event_list(trace_to_json.iter_lines_and_close())
    assert expected == [{'filename': 'utils.py',
                         'function': 'dummy_foo',
                         'kind': 'call',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': 'def dummy_foo(i=0):'},
                        {'filename': 'utils.py',
                         'function': 'dummy_foo',
                         'kind': 'line',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': '    i += 1'},
                        {'filename': 'utils.py',
                         'function': 'dummy_foo',
                         'kind': 'line',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': "    print(f'i: {i}')"},
                        {'filename': 'utils.py',
                         'function': 'dummy_foo',
                         'kind': 'return',
                         'module': 'trace_cockpit_testsite.utils',
                         'source': "    print(f'i: {i}')"}]
