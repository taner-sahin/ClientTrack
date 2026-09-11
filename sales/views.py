from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DealForm
from .models import Deal


@login_required
def deal_list(request):
    deals = Deal.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request,
        "sales/deal_list.html",
        {"deals": deals},
    )


@login_required
def deal_create(request):
    if request.method == "POST":
        form = DealForm(request.POST, user=request.user)

        if form.is_valid():
            deal = form.save(commit=False)
            deal.user = request.user
            deal.save()

            return redirect("sales:detail", pk=deal.pk)
    else:
        form = DealForm(user=request.user)

    return render(
        request,
        "sales/deal_form.html",
        {"form": form},
    )


@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(
        Deal,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "sales/deal_detail.html",
        {"deal": deal},
    )


@login_required
def deal_update(request, pk):
    deal = get_object_or_404(
        Deal,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = DealForm(
            request.POST,
            instance=deal,
            user=request.user,
        )

        if form.is_valid():
            deal = form.save(commit=False)
            deal.user = request.user
            deal.save()

            return redirect("sales:detail", pk=deal.pk)
    else:
        form = DealForm(
            instance=deal,
            user=request.user,
        )

    return render(
        request,
        "sales/deal_form.html",
        {"form": form},
    )


@login_required
def deal_delete(request, pk):
    deal = get_object_or_404(
        Deal,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        deal.delete()
        return redirect("sales:list")

    return render(
        request,
        "sales/deal_confirm_delete.html",
        {"deal": deal},
    )
