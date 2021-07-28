import hunter

from trace_cockpit.testutils import norm_json_event_list
from trace_cockpit.trace_to_json import TraceToJson


def foo():
    i = 0
    i += 1
    print(f'i: {i}')


def test_trace_to_json():
    trace_to_json = TraceToJson()
    with hunter.trace(trace_to_json):
        foo()
    expected = norm_json_event_list(trace_to_json.iter_lines_and_close())
    assert expected == [{'filename': 'test_trace_to_json.py',
                         'function': 'test_trace_to_json',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': '        foo()'},
                        {'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'call',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': 'def foo():'},
                        {'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': '    i = 0'},
                        {'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': '    i += 1'},
                        {'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': "    print(f'i: {i}')"},
                        {'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'return',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': "    print(f'i: {i}')"}]

