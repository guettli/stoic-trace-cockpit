import json
import os

from trace_cockpit import trace_to_json


def norm_json_event_list(event_list, include_only_these_modules=None):
    expected = []
    for line in event_list:
        if include_only_these_modules and (not line['module'] in include_only_these_modules):
            continue
        line['filename'] = os.path.basename(line['filename'])
        line.pop('lineno')
        line.pop('stdlib')
        line.pop('builtin')
        expected.append(line)
    return expected