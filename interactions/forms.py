from django import forms

from clients.models import Client

from .models import Interaction


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = (
            "client",
            "interaction_type",
            "subject",
            "notes",
            "interaction_date",
            "follow_up_date",
        )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        client_field = self.fields["client"]

        if isinstance(client_field, forms.ModelChoiceField):
            if user is not None:
                client_field.queryset = user.clients.order_by("name")
            else:
                client_field.queryset = Client.objects.none()
