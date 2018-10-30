from django import template

from ..models import *

register = template.Library()


@register.filter
def divide(a, b):
    return a % b


@register.filter
def has_answer(diag, person):
    if diag.has_answer(person):
        return "completed"
    else:
        return ""


@register.filter
def enrolled(course, person):
    return CourseUserRegistration.objects.filter(person=person, course=course).exists()
