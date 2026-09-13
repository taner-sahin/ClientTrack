from django.contrib import admin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "role",
        "owner",
        "is_active",
        "created_at",
    )
    list_filter = (
        "role",
        "is_active",
    )
    search_fields = (
        "name",
        "email",
        "owner__username",
    )
