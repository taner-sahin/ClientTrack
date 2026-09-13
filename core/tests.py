from django.test import TestCase
from django.urls import reverse


class CoreTests(TestCase):

    def test_security_overview_page_opens(self):
        response = self.client.get(reverse("core:security_overview"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "security_overview.html",
        )
