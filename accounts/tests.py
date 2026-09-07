from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthenticationTests(TestCase):

    def test_register_page_opens(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "register.html",
        )

    def test_login_page_opens(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "login.html",
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "first_name": "Taner",
                "last_name": "Şahin",
                "email": "taner@example.com",
                "username": "taner",
                "password1": "GucluParola123!",
                "password2": "GucluParola123!",
            },
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )

        user = User.objects.first()

        self.assertEqual(
            user.username,
            "taner",
        )

        self.assertEqual(
            user.first_name,
            "Taner",
        )

        self.assertEqual(
            user.last_name,
            "Şahin",
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
        )

    def test_user_cannot_register_with_different_passwords(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "first_name": "Taner",
                "last_name": "Şahin",
                "email": "taner@example.com",
                "username": "taner",
                "password1": "GucluParola123!",
                "password2": "FarkliParola123!",
            },
        )

        self.assertEqual(
            User.objects.count(),
            0,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_can_login(self):
        User.objects.create_user(
            username="taner",
            password="GucluParola123!",
            first_name="Taner",
            last_name="Şahin",
        )

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "taner",
                "password": "GucluParola123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:home"),
        )

        self.assertTrue("_auth_user_id" in self.client.session)

    def test_user_cannot_login_with_wrong_password(self):
        User.objects.create_user(
            username="taner",
            password="GucluParola123!",
        )

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "taner",
                "password": "YanlisParola123!",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertFalse("_auth_user_id" in self.client.session)

    def test_user_can_logout(self):
        User.objects.create_user(
            username="taner",
            password="GucluParola123!",
        )

        self.client.login(
            username="taner",
            password="GucluParola123!",
        )

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(
            response,
            reverse("core:home"),
        )

        self.assertFalse("_auth_user_id" in self.client.session)
