from django.conf import settings
from django.db import models

from clients.models import Client


class Interaction(models.Model):
    class InteractionType(models.TextChoices):
        PHONE = "phone", "Telefon"
        EMAIL = "email", "E-posta"
        MEETING = "meeting", "Toplantı"
        NOTE = "note", "Not"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
    )

    subject = models.CharField(max_length=200)

    notes = models.TextField(blank=True)

    interaction_date = models.DateTimeField()

    follow_up_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.name} - {self.subject}"
