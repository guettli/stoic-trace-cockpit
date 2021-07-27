import os

import hunter

from trace_cockpit.trace_to_json import TraceToJson


def foo():
    i = 0
    i += 1
    print(f'i: {i}')


def test_trace_to_json():
    trace_to_json = TraceToJson()
    with hunter.trace(trace_to_json):
        foo()
    expected = []
    for line in trace_to_json.read_and_close():
        line['filename'] = os.path.basename(line['filename'])
        line.pop('lineno')
        expected.append(line)
    assert expected == [{'builtin': False,
                         'filename': 'test_trace_to_json.py',
                         'function': 'test_trace_to_json',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': '        foo()',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'call',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': 'def foo():',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': '    i = 0',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': '    i += 1',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': "    print(f'i: {i}')",
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_trace_to_json.py',
                         'function': 'foo',
                         'kind': 'return',
                         'module': 'trace_cockpit.tests.test_trace_to_json',
                         'source': "    print(f'i: {i}')",
                         'stdlib': False}]
