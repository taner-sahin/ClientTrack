from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from clients.models import Client

from .models import Deal

User = get_user_model()


class DealTests(TestCase):
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

        self.deal1 = Deal.objects.create(
            user=self.user1,
            client=self.client1,
            title="User 1 Satış Fırsatı",
            stage=Deal.Stage.PROPOSAL,
            value="100000.00",
        )

        self.deal2 = Deal.objects.create(
            user=self.user2,
            client=self.client2,
            title="User 2 Satış Fırsatı",
            stage=Deal.Stage.NEGOTIATION,
            value="200000.00",
        )

    def test_deal_list_requires_login(self):
        response = self.client.get(reverse("sales:list"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('sales:list')}",
        )

    def test_deal_list_shows_only_logged_in_users_deals(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("sales:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.deal1.title)
        self.assertNotContains(response, self.deal2.title)

    def test_create_form_shows_only_logged_in_users_clients(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("sales:create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.client1.name)
        self.assertNotContains(response, self.client2.name)

    def test_deal_create_assigns_logged_in_user(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("sales:create"),
            {
                "client": self.client1.pk,
                "title": "Yeni Satış Fırsatı",
                "stage": Deal.Stage.QUALIFIED,
                "value": "150000.00",
                "expected_close_date": "2026-10-15",
                "notes": "Test fırsatı",
            },
        )

        deal = Deal.objects.get(title="Yeni Satış Fırsatı")

        self.assertRedirects(
            response,
            reverse("sales:detail", args=[deal.pk]),
        )
        self.assertEqual(deal.user, self.user1)
        self.assertEqual(deal.client, self.client1)

    def test_user_cannot_create_deal_for_another_users_client(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("sales:create"),
            {
                "client": self.client2.pk,
                "title": "Yetkisiz Satış Fırsatı",
                "stage": Deal.Stage.LEAD,
                "value": "50000.00",
                "expected_close_date": "",
                "notes": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Deal.objects.filter(title="Yetkisiz Satış Fırsatı").exists())

    def test_user_can_view_own_deal_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("sales:detail", args=[self.deal1.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.deal1.title)

    def test_user_cannot_view_another_users_deal_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("sales:detail", args=[self.deal2.pk]))

        self.assertEqual(response.status_code, 404)

    def test_user_can_update_own_deal(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("sales:update", args=[self.deal1.pk]),
            {
                "client": self.client1.pk,
                "title": "Güncellenmiş Satış Fırsatı",
                "stage": Deal.Stage.WON,
                "value": "175000.00",
                "expected_close_date": "2026-10-20",
                "notes": "Güncellendi",
            },
        )

        self.deal1.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("sales:detail", args=[self.deal1.pk]),
        )
        self.assertEqual(
            self.deal1.title,
            "Güncellenmiş Satış Fırsatı",
        )
        self.assertEqual(self.deal1.user, self.user1)

    def test_user_cannot_update_another_users_deal(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("sales:update", args=[self.deal2.pk]),
            {
                "client": self.client1.pk,
                "title": "Yetkisiz Güncelleme",
                "stage": Deal.Stage.WON,
                "value": "999999.00",
                "expected_close_date": "",
                "notes": "",
            },
        )

        self.deal2.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            self.deal2.title,
            "User 2 Satış Fırsatı",
        )

    def test_user_can_delete_own_deal(self):
        self.client.force_login(self.user1)

        response = self.client.post(reverse("sales:delete", args=[self.deal1.pk]))

        self.assertRedirects(response, reverse("sales:list"))
        self.assertFalse(Deal.objects.filter(pk=self.deal1.pk).exists())

    def test_user_cannot_delete_another_users_deal(self):
        self.client.force_login(self.user1)

        response = self.client.post(reverse("sales:delete", args=[self.deal2.pk]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Deal.objects.filter(pk=self.deal2.pk).exists())
