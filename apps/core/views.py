from django.shortcuts import render

from .models import Event


def index(request):
    context = dict()
    context["published_events"] = Event.objects.filter(status="p")
    return render(request, "index.html", context)
