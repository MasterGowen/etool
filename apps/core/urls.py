from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import index, dashboard, project, PersonUpdate

urlpatterns = [
    path('', login_required(index), name="index"),
    path('dashboard/', login_required(dashboard), name="dashboard"),
    path('person/', login_required(PersonUpdate.as_view()), name="person_update"),
    path('projects/<int:pk>/', project),
]
