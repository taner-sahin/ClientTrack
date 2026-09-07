from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ClientForm
from .models import Client


@login_required
def client_list(request):
    clients = Client.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "clients/client_list.html",
        {
            "clients": clients,
        },
    )


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)

            client.user = request.user
            client.save()

            return redirect("clients:list")

    else:
        form = ClientForm()

    return render(
    request,
    "clients/client_form.html",
    {
        "form": form,
        "page_title": "Yeni Müşteri",
        "page_description": "Yeni müşteri kaydınızı oluşturun.",
        "submit_label": "Müşteriyi Kaydet",
    },
)
    
@login_required
def client_detail(request, pk):
    client = get_object_or_404(
        Client,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "clients/client_detail.html",
        {
            "client": client,
        },
    )
    
@login_required
def client_update(request, pk):
    client = get_object_or_404(
        Client,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = ClientForm(
            request.POST,
            instance=client,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "clients:detail",
                pk=client.pk,
            )

    else:
        form = ClientForm(
            instance=client,
        )

    return render(
        request,
        "clients/client_form.html",
        {
            "form": form,
            "client": client,
            "page_title": "Müşteriyi Düzenle",
            "page_description": "Müşteri bilgilerini güncelleyin.",
            "submit_label": "Değişiklikleri Kaydet",
        },
    )
    
@login_required
def client_delete(request, pk):
    client = get_object_or_404(
        Client,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        client.delete()
        return redirect("clients:list")

    return render(
        request,
        "clients/client_confirm_delete.html",
        {
            "client": client,
        },
    )