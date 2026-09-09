from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clients.models import Client

from .models import Interaction

User = get_user_model()


class InteractionTests(TestCase):
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
        )

        self.interaction2 = Interaction.objects.create(
            user=self.user2,
            client=self.client2,
            interaction_type=Interaction.InteractionType.EMAIL,
            subject="User 2 Görüşmesi",
            interaction_date=timezone.now(),
        )

    def test_interaction_list_requires_login(self):
        response = self.client.get(reverse("interactions:list"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('interactions:list')}",
        )

    def test_interaction_list_shows_only_logged_in_users_interactions(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("interactions:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.interaction1.subject)
        self.assertNotContains(response, self.interaction2.subject)

    def test_create_form_shows_only_logged_in_users_clients(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("interactions:create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.client1.name)
        self.assertNotContains(response, self.client2.name)

    def test_interaction_create_assigns_logged_in_user(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("interactions:create"),
            {
                "client": self.client1.pk,
                "interaction_type": Interaction.InteractionType.MEETING,
                "subject": "Yeni Görüşme",
                "notes": "Test notu",
                "interaction_date": "2026-09-09 10:00:00",
                "follow_up_date": "",
            },
        )

        interaction = Interaction.objects.get(subject="Yeni Görüşme")

        self.assertRedirects(
            response,
            reverse("interactions:detail", args=[interaction.pk]),
        )
        self.assertEqual(interaction.user, self.user1)
        self.assertEqual(interaction.client, self.client1)

    def test_user_cannot_create_interaction_for_another_users_client(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("interactions:create"),
            {
                "client": self.client2.pk,
                "interaction_type": Interaction.InteractionType.PHONE,
                "subject": "Yetkisiz Görüşme",
                "notes": "",
                "interaction_date": "2026-09-09 10:00:00",
                "follow_up_date": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Interaction.objects.filter(subject="Yetkisiz Görüşme").exists()
        )

    def test_user_can_view_own_interaction_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse("interactions:detail", args=[self.interaction1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.interaction1.subject)

    def test_user_cannot_view_another_users_interaction_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse("interactions:detail", args=[self.interaction2.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_interaction(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("interactions:update", args=[self.interaction1.pk]),
            {
                "client": self.client1.pk,
                "interaction_type": Interaction.InteractionType.MEETING,
                "subject": "Güncellenmiş Görüşme",
                "notes": "Güncellendi",
                "interaction_date": "2026-09-09 11:00:00",
                "follow_up_date": "",
            },
        )

        self.interaction1.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("interactions:detail", args=[self.interaction1.pk]),
        )
        self.assertEqual(
            self.interaction1.subject,
            "Güncellenmiş Görüşme",
        )
        self.assertEqual(self.interaction1.user, self.user1)

    def test_user_cannot_update_another_users_interaction(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("interactions:update", args=[self.interaction2.pk]),
            {
                "client": self.client1.pk,
                "interaction_type": Interaction.InteractionType.NOTE,
                "subject": "Yetkisiz Güncelleme",
                "notes": "",
                "interaction_date": "2026-09-09 12:00:00",
                "follow_up_date": "",
            },
        )

        self.interaction2.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            self.interaction2.subject,
            "User 2 Görüşmesi",
        )

    def test_user_can_delete_own_interaction(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("interactions:delete", args=[self.interaction1.pk])
        )

        self.assertRedirects(response, reverse("interactions:list"))
        self.assertFalse(Interaction.objects.filter(pk=self.interaction1.pk).exists())

    def test_user_cannot_delete_another_users_interaction(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("interactions:delete", args=[self.interaction2.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Interaction.objects.filter(pk=self.interaction2.pk).exists())
