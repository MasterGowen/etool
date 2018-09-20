from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import index, dashboard, project, PersonUpdate, diagnostic, projects, diagnostics, a_persons

urlpatterns = [
    path('', login_required(index), name="index"),
    path('dashboard/', login_required(dashboard), name="dashboard"),
    path('person/', login_required(PersonUpdate.as_view()), name="person_update"),
    path('projects/<int:pk>/', project),
    path('projects/', projects),
    path('persons/', a_persons),
    path('diagnostics/', diagnostics),
    path('diagnostic/<int:pk>/', diagnostic),
]
