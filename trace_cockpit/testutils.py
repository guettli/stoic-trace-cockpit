import json
import os

from trace_cockpit import trace_to_json


def norm_json_lines(json_lines, include_only_these_modules=None):
    expected = []
    for line in json_lines:
        line = json.loads(line)
        if include_only_these_modules and (not line['module'] in include_only_these_modules):
            continue
        line['filename'] = os.path.basename(line['filename'])
        line.pop('lineno')
        line.pop('stdlib')
        line.pop('builtin')
        expected.append(line)
    return expected