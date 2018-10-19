from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path('', login_required(index), name="index"),
    path('dashboard/', login_required(dashboard), name="dashboard"),
    path('person/', login_required(PersonUpdate.as_view()), name="person_update"),
    path('projects/<int:pk>/', project),
    path('projects/', projects),
    path('persons/', a_persons, name="persons"),
    path('persons/activate/<int:pk>/', a_persons_activate),
    path('persons/deactivate/<int:pk>/', a_persons_deactivate),
    path('persons/recheck/<int:pk>/', a_diagnostic_recheck),
    path('persons/result/<int:pk>/', a_diagnostic_result),
    path('diagnostics/', diagnostics),
    path('diagnostic/<int:pk>/', diagnostic),
    path('my_diagnostic/<int:pk>/', my_diagnostic),

    path('events/', a_events, name="events"),
]
