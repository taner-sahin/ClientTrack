from django.urls import path

from . import views

app_name = "interactions"

urlpatterns = [
    path("", views.interaction_list, name="list"),
    path("new/", views.interaction_create, name="create"),
    path("<int:pk>/edit/", views.interaction_update, name="update"),
    path("<int:pk>/delete/", views.interaction_delete, name="delete"),
    path("<int:pk>/", views.interaction_detail, name="detail"),
]
