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


@register.filter
def have_theme(student, theme):
    if student in theme.students.all():
        return True
    return False


@register.filter
def for_course(themes, course):
    return [t for t in themes if t.course == course]


@register.filter
def for_course_len(themes, course):
    return len([t for t in themes if t.course == course])


@register.filter
def sort_by(queryset, order):
    res = []
    for i, e in queryset:
        res.append(e)
    return res.sort(key=lambda x: x.startdate, reverse=True)


@register.filter
def another_date(a, b):
    return a.startdate != b.startdate
