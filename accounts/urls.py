from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("team/", views.team_member_list, name="team_member_list"),
    path("team/new/", views.team_member_create, name="team_member_create"),
    path(
        "team/<int:pk>/",
        views.team_member_detail,
        name="team_member_detail",
    ),
    path(
        "team/<int:pk>/edit/",
        views.team_member_update,
        name="team_member_update",
    ),
    path(
        "team/<int:pk>/delete/",
        views.team_member_delete,
        name="team_member_delete",
    ),
]
