from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clients.models import Client
from interactions.models import Interaction
from sales.models import Deal

User = get_user_model()


class ReportsTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="Testpass123!",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Testpass123!",
        )

        self.client1 = Client.objects.create(
            user=self.user1,
            name="User 1 Müşterisi",
        )

        self.client2 = Client.objects.create(
            user=self.user2,
            name="User 2 Müşterisi",
        )

        self.interaction1 = Interaction.objects.create(
            user=self.user1,
            client=self.client1,
            interaction_type=Interaction.InteractionType.PHONE,
            subject="User 1 Görüşmesi",
            interaction_date=timezone.now(),
            follow_up_date=timezone.now() + timedelta(days=2),
        )

        self.interaction2 = Interaction.objects.create(
            user=self.user2,
            client=self.client2,
            interaction_type=Interaction.InteractionType.EMAIL,
            subject="User 2 Görüşmesi",
            interaction_date=timezone.now(),
            follow_up_date=timezone.now() + timedelta(days=3),
        )

        self.deal1 = Deal.objects.create(
            user=self.user1,
            client=self.client1,
            title="User 1 Açık Fırsat",
            stage=Deal.Stage.PROPOSAL,
            value="100000.00",
        )

        self.deal2 = Deal.objects.create(
            user=self.user1,
            client=self.client1,
            title="User 1 Kazanılan Fırsat",
            stage=Deal.Stage.WON,
            value="50000.00",
        )

        self.deal3 = Deal.objects.create(
            user=self.user2,
            client=self.client2,
            title="User 2 Fırsatı",
            stage=Deal.Stage.LOST,
            value="999999.00",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("reports:dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('reports:dashboard')}",
        )

    def test_dashboard_counts_only_logged_in_users_data(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("reports:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_clients"], 1)
        self.assertEqual(response.context["total_interactions"], 1)
        self.assertEqual(response.context["total_deals"], 2)

    def test_pipeline_value_uses_only_logged_in_users_deals(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("reports:dashboard"))

        self.assertEqual(
            response.context["total_pipeline_value"],
            150000,
        )

    def test_dashboard_deal_status_counts_are_correct(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("reports:dashboard"))

        self.assertEqual(response.context["open_deals"], 1)
        self.assertEqual(response.context["won_deals"], 1)
        self.assertEqual(response.context["lost_deals"], 0)

    def test_recent_interactions_are_user_isolated(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("reports:dashboard"))

        recent_interactions = response.context["recent_interactions"]

        self.assertIn(self.interaction1, recent_interactions)
        self.assertNotIn(self.interaction2, recent_interactions)

    def test_upcoming_followups_are_user_isolated(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("reports:dashboard"))

        upcoming_followups = response.context["upcoming_followups"]

        self.assertIn(self.interaction1, upcoming_followups)
        self.assertNotIn(self.interaction2, upcoming_followups)

    def test_stage_summary_contains_only_logged_in_users_deals(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("reports:dashboard"))

        stage_summary = list(response.context["stage_summary"])

        self.assertEqual(len(stage_summary), 2)

        stages = {item["stage"]: item["total"] for item in stage_summary}

        self.assertEqual(stages[Deal.Stage.PROPOSAL], 1)
        self.assertEqual(stages[Deal.Stage.WON], 1)
        self.assertNotIn(Deal.Stage.LOST, stages)
