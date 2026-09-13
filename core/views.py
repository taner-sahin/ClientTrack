from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def security_overview(request):
    return render(
        request,
        "security_overview.html",
    )
