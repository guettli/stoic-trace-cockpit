import json
import sys
from collections import defaultdict
from tempfile import NamedTemporaryFile, TemporaryFile

from hunter import CodePrinter, Action, Event


def is_stdlib(event: Event):
    # Issue https://github.com/ionelmc/python-hunter/issues/103
    is_stdlib = event.stdlib
    if not is_stdlib:
        return False
    if sys.prefix != sys.base_prefix:
        # In virtualenv
        if event.filename.startswith(sys.prefix):
            return False
    return True


def event_to_dict(event: Event):
    return dict(kind=event.kind, function=event.function, module=event.module,
                filename=event.filename, lineno=event.lineno, builtin=event.builtin,
                stdlib=is_stdlib(event), source=event.source.rstrip())

class TraceToJson(Action):
    stream = None

    skipped_modules: dict

    event_count_per_module: dict

    max_event_count_per_module = 100

    skipped_events_because_max_reached: dict

    def __init__(self, max_event_count_per_module=None):
        self.stream = TemporaryFile('w+t', encoding='utf8')
        self.skipped_modules = defaultdict(int)
        self.event_count_per_module = defaultdict(int)
        self.skipped_events_because_max_reached = defaultdict(int)

        if max_event_count_per_module is not None:
            self.max_event_count_per_module = max_event_count_per_module

    def __call__(self, event: Event):
        module = event.module
        if self.is_event_to_skip(event):
            self.skipped_modules[module] += 1
            return
        log_count = self.event_count_per_module[module]
        if log_count > self.max_event_count_per_module:
            self.skipped_events_because_max_reached[module] += 1
            return
        event = event_to_dict(event)
        log_count += 1
        if log_count == self.max_event_count_per_module:
            event['max_event_count_per_module_reached'] = True  # TODO: create nice visual marker in html output
        self.event_count_per_module[module] = log_count
        json.dump(event, self.stream)
        self.stream.write('\n')

    modules_to_skip = ['hunter', 'trace_cockpit', 'psycopg2', 'pytz', 'asgiref',
                       'django',

                       # TODO: enable/disable full/partial django skipping.
                       'django.template', 'django.utils', 'django.contrib.admin.templatetags',
                       'django.contrib.admin.utils', 'django.db.models.sql.compiler',
                       'django.utils.formats', 'django.db.models', 'django.urls.resolvers',
                       'django.forms', 'django.urls.base', 'django.contrib.admin.options',
                       'django.templatetags.i18n', 'django.middleware.csrf',
                       'django.contrib.admin.views.main', 'django.dispatch.dispatcher',
                       'django.apps.registry', 'django.http.response',
                       'django.db.backends', 'django.views.decorators.cache',
                       'django.templatetags.static',
                       'django.urls.converters',
                       'django.contrib.admin.helpers',
                        'django.db.utils', 'django.conf', 'django.contrib.staticfiles.storage',
                       'django.contrib.messages',
                       'django.contrib.sessions',
                       'django.core.signing',
                       'django.contrib.admin.sites',
                       'django.core.files.storage',

                                   ]
    _modules_to_skip_startswith = tuple(f'{module}.' for module in modules_to_skip)

    @classmethod
    def is_event_to_skip(cls, event: Event):
        if event.module in cls.modules_to_skip:
            return True
        if event.module.startswith(cls._modules_to_skip_startswith):
            return True
        if is_stdlib(event):
            return True
        return False

    def iter_lines_and_close(self):
        self.stream.seek(0)
        yield from self.stream
        self.stream.close()
