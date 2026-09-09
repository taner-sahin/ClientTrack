from django.contrib import admin

from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "client",
        "user",
        "interaction_type",
        "interaction_date",
        "follow_up_date",
    )

    search_fields = (
        "subject",
        "client__name",
        "user__username",
    )

    list_filter = (
        "interaction_type",
        "interaction_date",
        "follow_up_date",
    )
