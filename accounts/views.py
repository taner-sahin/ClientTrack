from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:login")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form},
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            return redirect("core:home")

    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "login.html",
        {"form": form},
    )


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect("core:home")