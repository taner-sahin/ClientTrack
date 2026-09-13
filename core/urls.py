from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "security/",
        views.security_overview,
        name="security_overview",
    ),
]
