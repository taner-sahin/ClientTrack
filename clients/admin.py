from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "email",
        "phone",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "user__username",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )