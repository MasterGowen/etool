from django.shortcuts import render
from django.views.generic.edit import UpdateView

from .models import Project, Person


def index(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    return render(request, "index.html", context)


def dashboard(request):
    context = dict()
    context["published_projects"] = Project.objects.filter(status="p")
    context["person"] = Person.objects.get(user=request.user)
    return render(request, "dashboard.html", context)


def project(request, pk):
    context = dict()
    context["project"] = Project.objects.get(pk=pk)
    context["person"] = Person.objects.get(user=request.user)
    return render(request, "project.html", context)


class PersonUpdate(UpdateView):
    model = Person
    success_url = '/dashboard'
    fields = ["first_name", "last_name", "second_name", "sex", "department", "group_number", "institute"]
    template_name = "person_form.html"

    def get(self, request, **kwargs):
        self.object = Person.objects.get(user=self.request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
