from django.urls import path

from .views import index, dashboard, project

urlpatterns = [
    path('', index, name="index"),
    path('dashboard/', dashboard, name="dashboard"),
    path('projects/<int:pk>/', project),
]
