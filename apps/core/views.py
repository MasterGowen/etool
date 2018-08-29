from django.shortcuts import render

from .models import Event, Project, Person


def index(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    return render(request, "index.html", context)


def dashboard(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    context["person"] = Person.objects.get(user=request.user)
    return render(request, "dashboard.html", context)
