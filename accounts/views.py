from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RegisterForm, TeamMemberForm
from .models import TeamMember


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


@login_required
def team_member_list(request):
    team_members = TeamMember.objects.filter(
        owner=request.user,
    ).order_by("name")

    return render(
        request,
        "accounts/team_member_list.html",
        {"team_members": team_members},
    )


@login_required
def team_member_create(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST)

        if form.is_valid():
            team_member = form.save(commit=False)
            team_member.owner = request.user
            team_member.save()

            return redirect("accounts:team_member_list")

    else:
        form = TeamMemberForm()

    return render(
        request,
        "accounts/team_member_form.html",
        {
            "form": form,
            "title": "Takım Üyesi Ekle",
        },
    )


@login_required
def team_member_detail(request, pk):
    team_member = get_object_or_404(
        TeamMember,
        pk=pk,
        owner=request.user,
    )

    return render(
        request,
        "accounts/team_member_detail.html",
        {"team_member": team_member},
    )


@login_required
def team_member_update(request, pk):
    team_member = get_object_or_404(
        TeamMember,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":
        form = TeamMemberForm(
            request.POST,
            instance=team_member,
        )

        if form.is_valid():
            form.save()
            return redirect(
                "accounts:team_member_detail",
                pk=team_member.pk,
            )

    else:
        form = TeamMemberForm(instance=team_member)

    return render(
        request,
        "accounts/team_member_form.html",
        {
            "form": form,
            "title": "Takım Üyesini Düzenle",
        },
    )


@login_required
def team_member_delete(request, pk):
    team_member = get_object_or_404(
        TeamMember,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":
        team_member.delete()
        return redirect("accounts:team_member_list")

    return render(
        request,
        "accounts/team_member_confirm_delete.html",
        {"team_member": team_member},
    )
