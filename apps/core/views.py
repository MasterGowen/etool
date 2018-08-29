from django.shortcuts import render

from .models import Event, Project


def index(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    return render(request, "index.html", context)
