from django import template

register = template.Library()

@register.filter
def dot(value):
    return value.replace(",", ".")
