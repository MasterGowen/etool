from django.urls import path

from .views import index, dashboard, project, PersonUpdate

urlpatterns = [
    path('', index, name="index"),
    path('dashboard/', dashboard, name="dashboard"),
    path('person/', PersonUpdate.as_view(), name="person_update"),
    path('projects/<int:pk>/', project),
]
