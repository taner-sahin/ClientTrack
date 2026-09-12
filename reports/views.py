from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from clients.models import Client
from interactions.models import Interaction
from sales.models import Deal


@login_required
def dashboard(request):
    clients = Client.objects.filter(user=request.user)
    interactions = Interaction.objects.filter(user=request.user)
    deals = Deal.objects.filter(user=request.user)

    total_clients = clients.count()
    total_interactions = interactions.count()
    total_deals = deals.count()

    total_pipeline_value = deals.aggregate(total=Sum("value"))["total"] or 0

    open_deals = deals.exclude(stage__in=[Deal.Stage.WON, Deal.Stage.LOST]).count()

    won_deals = deals.filter(stage=Deal.Stage.WON).count()
    lost_deals = deals.filter(stage=Deal.Stage.LOST).count()

    stage_summary = deals.values("stage").annotate(total=Count("id")).order_by("stage")

    recent_interactions = interactions.select_related("client").order_by(
        "-interaction_date"
    )[:5]

    upcoming_followups = (
        interactions.filter(follow_up_date__gte=timezone.now())
        .select_related("client")
        .order_by("follow_up_date")[:5]
    )

    context = {
        "total_clients": total_clients,
        "total_interactions": total_interactions,
        "total_deals": total_deals,
        "total_pipeline_value": total_pipeline_value,
        "open_deals": open_deals,
        "won_deals": won_deals,
        "lost_deals": lost_deals,
        "stage_summary": stage_summary,
        "recent_interactions": recent_interactions,
        "upcoming_followups": upcoming_followups,
    }

    return render(
        request,
        "reports/dashboard.html",
        context,
    )
