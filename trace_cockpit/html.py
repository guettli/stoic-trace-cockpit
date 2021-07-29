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
</style>
'''

def jsontrace_to_html__iter(jsontrace):
    yield css
    for line in jsontrace:
        yield jsontrace_line_to_html(line)

def jsontrace_line_to_html(line):
    kind = line['kind']
    if kind == 'call':
        return jsontrace_line_to_html__call(line)
    if kind == 'line':
        return jsontrace_line_to_html__line(line)
    if kind == 'return':
        return ''
        #return jsontrace_line_to_html__return(line)
    raise Exception(f'Unknown kind: {kind}')

def jsontrace_line_to_html__call(line):
    return format_html('''
   <div class="dtc-line">
    <span class="dtc-kind">{kind}</span>
    <span class="dtc-module">{module}</span>
    <span class="dtc-filename">{filename}</span>
    <span class="dtc-lineno">{lineno}</span>
    <span class="dtc-source">{source}</span>
   </div>
    ''', **line)

def jsontrace_line_to_html__line(line):
    return format_html('''
   <div class="dtc-line">
    <span class="dtc-kind">{kind}</span>
    <span class="dtc-module">{module}</span>
    <span class="dtc-filename">{filename}</span>
    <span class="dtc-lineno">{lineno}</span>
    <span class="dtc-source">{source}</span>
   </div>
    ''', **line)


def jsontrace_line_to_html__return(line):
    return format_html('''
   <div class="dtc-line">
    <span class="dtc-kind">{kind}</span>
    <span class="dtc-module">{module}</span>
    <span class="dtc-filename">{filename}</span>
    <span class="dtc-lineno">{lineno}</span>
    <span class="dtc-source">{source}</span>
   </div>
    ''', **line)