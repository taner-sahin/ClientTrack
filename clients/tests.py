from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Client


User = get_user_model()


class ClientTests(TestCase):
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
            email="user1client@example.com",
        )

        self.client2 = Client.objects.create(
            user=self.user2,
            name="User 2 Müşterisi",
            email="user2client@example.com",
        )

    def test_client_list_requires_login(self):
        response = self.client.get(
            reverse("clients:list")
        )

        expected_url = (
            f"{reverse('accounts:login')}"
            f"?next={reverse('clients:list')}"
        )

        self.assertRedirects(
            response,
            expected_url,
        )

    def test_client_list_shows_only_logged_in_users_clients(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse("clients:list")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            self.client1.name,
        )

        self.assertNotContains(
            response,
            self.client2.name,
        )

    def test_client_create_assigns_logged_in_user(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("clients:create"),
            {
                "name": "Yeni Müşteri",
                "email": "newclient@example.com",
                "phone": "",
                "website": "",
                "address": "",
                "notes": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("clients:list"),
        )

        created_client = Client.objects.get(
            name="Yeni Müşteri",
        )

        self.assertEqual(
            created_client.user,
            self.user1,
        )

    def test_user_can_view_own_client_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                "clients:detail",
                kwargs={"pk": self.client1.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            self.client1.name,
        )

    def test_user_cannot_view_another_users_client_detail(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                "clients:detail",
                kwargs={"pk": self.client2.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_user_can_update_own_client(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse(
                "clients:update",
                kwargs={"pk": self.client1.pk},
            ),
            {
                "name": "Güncellenmiş Müşteri",
                "email": "updated@example.com",
                "phone": "",
                "website": "",
                "address": "",
                "notes": "",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "clients:detail",
                kwargs={"pk": self.client1.pk},
            ),
        )

        self.client1.refresh_from_db()

        self.assertEqual(
            self.client1.name,
            "Güncellenmiş Müşteri",
        )

        self.assertEqual(
            self.client1.user,
            self.user1,
        )

    def test_user_cannot_update_another_users_client(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse(
                "clients:update",
                kwargs={"pk": self.client2.pk},
            ),
            {
                "name": "Yetkisiz Güncelleme",
                "email": "hacked@example.com",
                "phone": "",
                "website": "",
                "address": "",
                "notes": "",
            },
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.client2.refresh_from_db()

        self.assertEqual(
            self.client2.name,
            "User 2 Müşterisi",
        )
         
    def test_user_can_delete_own_client(self):
     self.client.force_login(self.user1)

     response = self.client.post(
        reverse(
            "clients:delete",
            kwargs={"pk": self.client1.pk},
        )
    )

     self.assertRedirects(
        response,
        reverse("clients:list"),
    )

     self.assertFalse(
        Client.objects.filter(pk=self.client1.pk).exists()
    )


    def test_user_cannot_delete_another_users_client(self):
     self.client.force_login(self.user1)

     response = self.client.post(
        reverse(
            "clients:delete",
            kwargs={"pk": self.client2.pk},
        )
    )

     self.assertEqual(
        response.status_code,
        404,
    )

     self.assertTrue(
        Client.objects.filter(pk=self.client2.pk).exists()
    )      