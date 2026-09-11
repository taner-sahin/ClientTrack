from django.contrib import admin

from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "user",
        "stage",
        "value",
        "expected_close_date",
        "created_at",
    )

    search_fields = (
        "title",
        "client__name",
        "user__username",
    )

    list_filter = (
        "stage",
        "expected_close_date",
        "created_at",
    )
