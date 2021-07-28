import json
import sys
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

    def __init__(self):
        self.stream = TemporaryFile('w+t', encoding='utf8')

    def __call__(self, event: Event):
        if self.is_event_to_skip(event):
            return
        json.dump(event_to_dict(event), self.stream)
        self.stream.write('\n')

    @classmethod
    def is_event_to_skip(cls, event: Event):
        if event.module.startswith(('hunter.', 'hunter', 'trace_cockpit.', 'django.', 'asgiref.')):
            return True
        if is_stdlib(event):
            return True
        return False

    def iter_lines_and_close(self):
        self.stream.seek(0)
        for line in self.stream:
            yield json.loads(line)
        self.stream.close()
