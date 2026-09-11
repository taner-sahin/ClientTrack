from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path("", views.deal_list, name="list"),
    path("new/", views.deal_create, name="create"),
    path("<int:pk>/edit/", views.deal_update, name="update"),
    path("<int:pk>/delete/", views.deal_delete, name="delete"),
    path("<int:pk>/", views.deal_detail, name="detail"),
]
