import pytest
from django.urls import reverse

from trace_cockpit.models import TraceConfig, TraceLog
from trace_cockpit.testutils import norm_json_event_list


def foo(i):
    return i + 1


@pytest.mark.django_db
def test_TraceConfig_trace():
    config = TraceConfig.objects.create(name='foo')
    log, _ = config.trace(foo, 1)
    log = TraceLog.objects.get(id=log.id)
    assert log.config == config
    expected = norm_json_event_list(log.json)
    assert expected == [{'filename': 'models.py',
                         'function': 'trace',
                         'kind': 'line',
                         'module': 'trace_cockpit.models',
                         'source': '            ret = function(*args, **kwargs)'},
                        {'filename': 'test_models.py',
                         'function': 'foo',
                         'kind': 'call',
                         'module': 'trace_cockpit.tests.test_models',
                         'source': 'def foo(i):'},
                        {'filename': 'test_models.py',
                         'function': 'foo',
                         'kind': 'line',
                         'module': 'trace_cockpit.tests.test_models',
                         'source': '    return i + 1'},
                        {'filename': 'test_models.py',
                         'function': 'foo',
                         'kind': 'return',
                         'module': 'trace_cockpit.tests.test_models',
                         'source': '    return i + 1'}]


@pytest.mark.django_db
def test_dummy_view(client):
    config = TraceConfig.objects.create(name='dummy')
    url = reverse('dummy_view')
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == b'<html><body>i: 1</body></html>'
    log = TraceLog.objects.get(config=config)
    assert norm_json_event_list(log.json, include_only_these_modules=['trace_cockpit_testsite.urls']) == \
           [{'filename': 'urls.py',
             'function': 'dummy_view',
             'kind': 'call',
             'module': 'trace_cockpit_testsite.urls',
             'source': 'def dummy_view(request):'},
            {'filename': 'urls.py',
             'function': 'dummy_view',
             'kind': 'line',
             'module': 'trace_cockpit_testsite.urls',
             'source': '    i = 0'},
            {'filename': 'urls.py',
             'function': 'dummy_view',
             'kind': 'line',
             'module': 'trace_cockpit_testsite.urls',
             'source': '    i += 1'},
            {'filename': 'urls.py',
             'function': 'dummy_view',
             'kind': 'line',
             'module': 'trace_cockpit_testsite.urls',
             'source': "    return HttpResponse(f'<html><body>i: {i}</body></html>')"},
            {'filename': 'urls.py',
             'function': 'dummy_view',
             'kind': 'return',
             'module': 'trace_cockpit_testsite.urls',
             'source': "    return HttpResponse(f'<html><body>i: {i}</body></html>')"}]
