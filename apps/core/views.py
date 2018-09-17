import json

from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView

from .models import Project, Person, Diagnostic, StudentDiag


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

        print(request.POST)

        SD = StudentDiag.objects.create(
            diagnostic=diagnostic,
            person=person,
            answer=answer
        )
        return redirect("/dashboard")


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
