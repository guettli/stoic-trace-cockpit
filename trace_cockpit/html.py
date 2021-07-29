import json

from django.utils.html import format_html
from django.utils.safestring import mark_safe


def jsontrace_to_html(jsontrace):
    return mark_safe(''.join(jsontrace_to_html__iter(jsontrace)))

css = '''
<style>
.dtc-source {
    white-space: pre;
    font-family: monospace;
    }
.dtc-filename {
    width: 20em;
    direction: rtl;
    text-overflow: ellipsis;
}     
.dtc-lineno {
   width: 4em;
   text-align: right;
}
.dtc-kind-call {
    margin-top: 2em;
}
</style>
'''

def jsontrace_to_html__iter(jsontrace):
    yield css
    for line in jsontrace:
        yield jsontrace_line_to_html(line)

def filename_to_html(filename, module):
    return format_html('<span class="dtc-filename" title="{filename} ({module})">...{truncated}</span>', filename=filename,
                       truncated=filename[-40:], module=module)

def jsontrace_line_to_html(line):
    line = json.loads(line)
    kind = line['kind']
    line['filename'] = filename_to_html(line['filename'], line['module'])
    if kind == 'call':
        return jsontrace_line_to_html__line(line)
    if kind == 'line':
        return jsontrace_line_to_html__line(line)
    if kind == 'return':
        return mark_safe('<br>')
        #return jsontrace_line_to_html__return(line)
    if kind == 'exception':
        return jsontrace_line_to_html__line(line)
    raise Exception(f'Unknown kind: {kind}')


def jsontrace_line_to_html__line(line):
    return format_html('''
   <div class="dtc-line dtc-kind-{kind}">
    <span class="dtc-kind">{kind}</span>
    {filename}
    <span class="dtc-lineno">{lineno}</span>
    <span class="dtc-source">{source}</span>
   </div>
    ''', **line)

