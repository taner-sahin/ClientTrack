from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import TeamMember, User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class TeamMemberForm(forms.ModelForm):

    class Meta:
        model = TeamMember
        fields = (
            "name",
            "email",
            "role",
            "is_active",
        )
