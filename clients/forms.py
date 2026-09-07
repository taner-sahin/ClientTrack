from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

        fields = (
            "name",
            "email",
            "phone",
            "website",
            "address",
            "notes",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Örn: Acme Yazılım",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ornek@firma.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+90 555 000 00 00",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com",
                }
            ),
            "address": forms.Textarea(
    attrs={
        "class": "form-control",
        "rows": 2,
        "placeholder": "Adres bilgisi",
    }
),
"notes": forms.Textarea(
    attrs={
        "class": "form-control",
        "rows": 3,
        "placeholder": "Müşteri hakkında notlar",
    }
),
        }