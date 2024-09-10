from django import template

register = template.Library()


@register.simple_tag
def add_path(data):
    if data:
        return f'/media/{data}'
    return '#'
