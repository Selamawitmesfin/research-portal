from django.urls import path

from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("projects/", views.project_list, name="project_list"),
    path("datasets/", views.dataset_list, name="dataset_list"),
    path("papers/", views.paper_list, name="paper_list"),
    path(
        "projects/<int:project_id>/",
        views.project_resources,
        name="project_resources",
    ),
    path("upload/", views.resource_upload, name="resource_upload"),
]
