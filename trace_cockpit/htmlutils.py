from django.utils.html import format_html
from stoic_html import join


def count_dict_to_html(count_dict):
    rows = []
    for name, count in sorted(count_dict.items(), key=lambda key_value: key_value[1], reverse=True):
        rows.append(format_html('<tr><td>{name}</td><td>{count}</td></tr>', name=name, count=count))
    if not rows:
        return ''
    return format_html('<table><tr><th>Module</th><th>Lines of Code</th></tr>{rows}</table>', rows=join(rows))
