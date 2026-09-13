from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class TeamMember(models.Model):
    class Role(models.TextChoices):
        MANAGER = "manager", "Yönetici"
        SALES = "sales", "Satış"
        SUPPORT = "support", "Destek"
        OTHER = "other", "Diğer"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_members",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OTHER,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
