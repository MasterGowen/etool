from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView

from .models import *


def index(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    if request.user.is_authenticated:
        context["person"] = Person.objects.get(user=request.user)
        return redirect("/dashboard")
    else:
        context["person"] = None
    return render(request, "index.html", context)


def dashboard(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    context["person"] = Person.objects.get(user=request.user)
    if request.user.is_staff:
        context["diagnostics"] = Diagnostic.objects.order_by("weight")
    else:
        context["diagnostics"] = Diagnostic.objects.filter(published="p").order_by("weight")
    if not context["person"].is_full():
        return redirect("/person?next=/dashboard")
    return render(request, "dashboard.html", context)


def project(request, pk):
    context = dict()
    context["project"] = Project.objects.get(pk=pk)
    if request.user.is_staff:
        context["diagnostics"] = Diagnostic.objects.order_by("weight")
    else:
        context["diagnostics"] = Diagnostic.objects.filter(published="p").order_by("weight")
    context["person"] = Person.objects.get(user=request.user)
    return render(request, "project.html", context)


def projects(request):
    context = dict()
    context["projects"] = Project.objects.all()
    if request.user.is_staff:
        context["diagnostics"] = Diagnostic.objects.order_by("weight")
    else:
        context["diagnostics"] = Diagnostic.objects.filter(published="p").order_by("weight")
    context["person"] = Person.objects.get(user=request.user)
    return render(request, "projects.html", context)


def diagnostics(request):
    context = dict()
    context["projects"] = Project.objects.all()
    if request.user.is_staff:
        context["diagnostics"] = Diagnostic.objects.order_by("weight")
    else:
        context["diagnostics"] = Diagnostic.objects.filter(published="p").order_by("weight")
    context["person"] = Person.objects.get(user=request.user)
    return render(request, "diagnostics.html", context)


def diagnostic(request, pk):
    if request.method == "GET":
        context = dict()
        context["diagnostic"] = Diagnostic.objects.get(pk=pk)
        if request.user.is_staff:
            context["diagnostics"] = Diagnostic.objects.order_by("weight")
        else:
            context["diagnostics"] = Diagnostic.objects.filter(published="p").order_by("weight")
        context["person"] = Person.objects.get(user=request.user)
        return render(request, "diagnostic.html", context)
    elif request.method == "POST":
        diagnostic = Diagnostic.objects.get(pk=pk)
        person = Person.objects.get(user=request.user)

        answer = json.dumps(request.POST)

        SD = StudentDiag.objects.create(
            diagnostic=diagnostic,
            person=person,
            answer=answer
        )

        q = json.loads(SD.answer)
        q.pop('csrfmiddlewaretoken', None)
        SD.answer = json.dumps(q)
        return redirect("/dashboard")


def my_diagnostic(request, pk):
    sd = StudentDiag.objects.filter(person__user=request.user, diagnostic__id=pk)
    return render(request, "d_result.html", {"sd": sd})


def a_persons_activate(request, pk):
    if request.method == "GET":
        p = Person.objects.get(pk=pk)
        p.checked = True
        p.save()
        return redirect("persons")


def a_persons_deactivate(request, pk):
    if request.method == "GET":
        p = Person.objects.get(pk=pk)
        p.checked = False
        p.save()
        return redirect("persons")


def a_diagnostic_recheck(request, pk):
    if request.method == "GET":
        sd = StudentDiag.objects.get(pk=pk)
        sd.send()
        return redirect("persons")


def a_diagnostic_result(request, pk):
    if request.method == "GET":
        sd = StudentDiag.objects.get(pk=pk)
        return render(request, "d_result.html", {"sd": sd})


class PersonUpdate(UpdateView):
    model = Person
    success_url = '/dashboard'
    fields = ["first_name", "last_name", "second_name", "sex", "institute", "department", "group_number", ]
    template_name = "person_form.html"

    def get_object(self, queryset=None):
        return Person.objects.get(user=self.request.user)

    def get(self, request, **kwargs):
        self.object = Person.objects.get(user=self.request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@staff_member_required
def a_persons(request):
    context = dict()
    context["persons"] = Person.objects.filter(user__is_staff=False)
    context["person"] = Person.objects.get(user=request.user)
    context["diagnostics"] = Diagnostic.objects.all()
    return render(request, "a_persons.html", context)


@staff_member_required
def a_events(request):
    context = dict()
    context["persons"] = Person.objects.filter(user__is_staff=False)
    context["person"] = Person.objects.get(user=request.user)
    context["diagnostics"] = Diagnostic.objects.all()
    context["projects"] = Project.objects.all()
    return render(request, "a_events.html", context)


@staff_member_required
def a_events_visit(request, project_pk, pk):
    event = Event.objects.get(pk=pk)
    project = Project.objects.get(pk=project_pk)

    context = dict()
    context["project"] = project
    context["event"] = event
    context["persons"] = Person.objects.filter(user__is_staff=False)
    context["event_registrations"] = event.get_students()
    context["project_registrations"] = event.get_project_students()
    context["visits"] = Visit.objects.filter(event=event, project=project)
    return render(request, "a_event_visit.html", context)


@staff_member_required
def a_events_visit_add(request, project_pk, pk, person_pk):
    event = Event.objects.get(pk=pk)
    project = Project.objects.get(pk=project_pk)
    person = Person.objects.get(pk=person_pk)

    Visit.objects.create(event=event, person=person, project=project)
    return redirect("events_visit", project_pk=project_pk, pk=pk)


@staff_member_required
def a_events_visit_remove(request, project_pk, pk, person_pk):
    event = Event.objects.get(pk=pk)
    project = Project.objects.get(pk=project_pk)
    person = Person.objects.get(pk=person_pk)

    Visit.objects.filter(event=event, person=person, project=project).delete()
    return redirect("events_visit", project_pk=project_pk, pk=pk)
