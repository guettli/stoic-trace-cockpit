import pytest

from trace_cockpit.models import TraceConfig, TraceLog
from trace_cockpit.testutils import norm_json_event_list


def foo(i):
    return i + 1


@pytest.mark.django_db
def test_TraceConfig_trace():
    config = TraceConfig.objects.create(name='foo')
    log = config.trace(foo, 1)
    log = TraceLog.objects.get(id=log.id)
    assert log.config == config
    expected = norm_json_event_list(log.json)
    assert expected == [{'builtin': False,
                         'filename': 'models.py',
                         'function': 'trace',
                         'kind': 'line',
                         'module': 'trace_cockpit.models',
                         'source': '            function(*args, **kwargs)',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_models.py',
                         'function': 'foo',
                         'kind': 'call',
                         'module': 'trace_cockpit.tests.test_models',
                         'source': 'def foo(i):',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_models.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_models',
                         'source': '    return i + 1',
                         'stdlib': False},
                        {'builtin': False,
                         'filename': 'test_models.py',
                         'function': 'foo',
                         'kind': 'return',
                         'module': 'trace_cockpit.tests.test_models',
                         'source': '    return i + 1',
                         'stdlib': False}]
