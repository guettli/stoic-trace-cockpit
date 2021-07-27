import json
import os

from trace_cockpit import trace_to_json


def norm_json_event_list(event_list):
    expected = []
    for line in event_list:
        line['filename'] = os.path.basename(line['filename'])
        line.pop('lineno')
        expected.append(line)
    return expected