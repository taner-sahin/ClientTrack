from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import InteractionForm
from .models import Interaction


@login_required
def interaction_list(request):
    interactions = Interaction.objects.filter(user=request.user).order_by(
        "-interaction_date"
    )

    return render(
        request,
        "interactions/interaction_list.html",
        {"interactions": interactions},
    )


@login_required
def interaction_create(request):
    if request.method == "POST":
        form = InteractionForm(request.POST, user=request.user)

        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user = request.user
            interaction.save()

            return redirect("interactions:detail", pk=interaction.pk)
    else:
        form = InteractionForm(user=request.user)

    return render(
        request,
        "interactions/interaction_form.html",
        {"form": form},
    )


@login_required
def interaction_detail(request, pk):
    interaction = get_object_or_404(
        Interaction,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "interactions/interaction_detail.html",
        {"interaction": interaction},
    )


@login_required
def interaction_update(request, pk):
    interaction = get_object_or_404(
        Interaction,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        form = InteractionForm(
            request.POST,
            instance=interaction,
            user=request.user,
        )

        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.user = request.user
            interaction.save()

            return redirect("interactions:detail", pk=interaction.pk)
    else:
        form = InteractionForm(
            instance=interaction,
            user=request.user,
        )

    return render(
        request,
        "interactions/interaction_form.html",
        {"form": form},
    )


@login_required
def interaction_delete(request, pk):
    interaction = get_object_or_404(
        Interaction,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":
        interaction.delete()
        return redirect("interactions:list")

    return render(
        request,
        "interactions/interaction_confirm_delete.html",
        {"interaction": interaction},
    )


@login_required
def reminder_list(request):
    now = timezone.now()

    upcoming_followups = (
        Interaction.objects.filter(
            user=request.user,
            follow_up_date__gte=now,
            follow_up_completed=False,
        )
        .select_related("client")
        .order_by("follow_up_date")
    )

    overdue_followups = (
        Interaction.objects.filter(
            user=request.user,
            follow_up_date__lt=now,
            follow_up_completed=False,
        )
        .select_related("client")
        .order_by("follow_up_date")
    )

    completed_followups = (
        Interaction.objects.filter(
            user=request.user,
            follow_up_date__isnull=False,
            follow_up_completed=True,
        )
        .select_related("client")
        .order_by("-follow_up_date")
    )

    context = {
        "upcoming_followups": upcoming_followups,
        "overdue_followups": overdue_followups,
        "completed_followups": completed_followups,
    }

    return render(
        request,
        "interactions/reminder_list.html",
        context,
    )


@login_required
@require_POST
def follow_up_complete(request, pk):
    interaction = get_object_or_404(
        Interaction,
        pk=pk,
        user=request.user,
    )

    interaction.follow_up_completed = True
    interaction.save(update_fields=["follow_up_completed"])

    return redirect("interactions:reminders")
