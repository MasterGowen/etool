from django import template

register = template.Library()


@register.filter
def divide(a, b):
    return b % a


@register.filter
def has_answer(diag, person):
    if diag.has_answer(person):
        return "completed"
    else:
        return ""
