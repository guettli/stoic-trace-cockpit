import pytest
from django.urls import reverse

from trace_cockpit.models import TraceConfig, TraceLog
from trace_cockpit.testutils import norm_json_lines
from trace_cockpit_testsite.utils import dummy_get_response


@pytest.mark.django_db
def test_trace_get_response(rf):
    config = TraceConfig.objects.create(name='foo')
    log, response = config.trace_get_response(dummy_get_response, rf.get('/path?arg=value'))
    log = TraceLog.objects.get(id=log.id)
    assert log.config == config
    assert log.url == '/path?arg=value'
    assert log.http_status == '200: OK'
    expected = norm_json_lines(log.json_lines.splitlines())
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


@pytest.mark.django_db
def test_dummy_view(client):
    config = TraceConfig.objects.create(name='dummy')
    url = reverse('dummy_view')
    response = client.get(url)
    assert response.status_code == 200
    assert response.content == b'<html><body>i: 1</body></html>'
    log = TraceLog.objects.get(config=config)
    assert log.http_method == 'GET'
    assert log.http_status == '200: OK'
    expected = \
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
    assert norm_json_lines(log.json_lines.splitlines(), include_only_these_modules=['trace_cockpit_testsite.urls']) == expected


@pytest.mark.django_db
def test_do_you_want_to_trace__eval_exception(rf):
    config = TraceConfig.objects.create(trace_request_eval='foo(')
    assert not config.do_you_want_to_trace(rf.get('/'))
    log = TraceLog.objects.get(config=config)
    assert not log.success
    assert log.error_message == 'Eval failed: unexpected EOF while parsing (<string>, line 1)'

    config.trace_request_eval = "'fooo' in url"
    assert config.do_you_want_to_trace(rf.get('/?fooo'))
    assert not config.do_you_want_to_trace(rf.get('/?bar'))
