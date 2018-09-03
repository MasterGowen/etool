from django import template

register = template.Library()


@register.filter
def divide(a, b):
    return b % a
