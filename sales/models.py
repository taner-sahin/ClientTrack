from django.conf import settings
from django.db import models

from clients.models import Client


class Deal(models.Model):
    class Stage(models.TextChoices):
        LEAD = "lead", "Potansiyel"
        QUALIFIED = "qualified", "Nitelikli"
        PROPOSAL = "proposal", "Teklif"
        NEGOTIATION = "negotiation", "Müzakere"
        WON = "won", "Kazanıldı"
        LOST = "lost", "Kaybedildi"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="deals",
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="deals",
    )

    title = models.CharField(max_length=200)

    stage = models.CharField(
        max_length=20,
        choices=Stage.choices,
        default=Stage.LEAD,
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    expected_close_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.name} - {self.title}"
