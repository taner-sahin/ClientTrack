from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import TeamMember

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


class TeamMemberTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="TestPassword123!",
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="TestPassword123!",
        )

        self.member1 = TeamMember.objects.create(
            owner=self.user1,
            name="Ayşe Yılmaz",
            email="ayse@example.com",
            role=TeamMember.Role.SALES,
            is_active=True,
        )

        self.member2 = TeamMember.objects.create(
            owner=self.user2,
            name="Mehmet Demir",
            email="mehmet@example.com",
            role=TeamMember.Role.SUPPORT,
            is_active=True,
        )

    def test_team_member_list_requires_login(self):
        response = self.client.get(reverse("accounts:team_member_list"))

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_team_member_list_shows_only_logged_in_users_members(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse("accounts:team_member_list"))

        team_members = response.context["team_members"]

        self.assertIn(
            self.member1,
            team_members,
        )

        self.assertNotIn(
            self.member2,
            team_members,
        )

    def test_user_can_create_team_member_with_ownership(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("accounts:team_member_create"),
            {
                "name": "Burak Kaya",
                "email": "burak@example.com",
                "role": TeamMember.Role.MANAGER,
                "is_active": True,
            },
        )

        team_member = TeamMember.objects.get(email="burak@example.com")

        self.assertEqual(
            team_member.owner,
            self.user1,
        )

        self.assertRedirects(
            response,
            reverse("accounts:team_member_list"),
        )

    def test_user_can_view_own_team_member(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                "accounts:team_member_detail",
                args=[self.member1.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.context["team_member"],
            self.member1,
        )

    def test_user_cannot_view_another_users_team_member(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                "accounts:team_member_detail",
                args=[self.member2.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_user_can_update_own_team_member(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse(
                "accounts:team_member_update",
                args=[self.member1.pk],
            ),
            {
                "name": "Ayşe Güncellendi",
                "email": "ayse@example.com",
                "role": TeamMember.Role.MANAGER,
                "is_active": True,
            },
        )

        self.member1.refresh_from_db()

        self.assertEqual(
            self.member1.name,
            "Ayşe Güncellendi",
        )

        self.assertEqual(
            self.member1.role,
            TeamMember.Role.MANAGER,
        )

        self.assertRedirects(
            response,
            reverse(
                "accounts:team_member_detail",
                args=[self.member1.pk],
            ),
        )

    def test_user_cannot_update_another_users_team_member(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse(
                "accounts:team_member_update",
                args=[self.member2.pk],
            ),
            {
                "name": "Yetkisiz Güncelleme",
                "email": "mehmet@example.com",
                "role": TeamMember.Role.MANAGER,
                "is_active": True,
            },
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.member2.refresh_from_db()

        self.assertEqual(
            self.member2.name,
            "Mehmet Demir",
        )

    def test_user_can_delete_own_team_member(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse(
                "accounts:team_member_delete",
                args=[self.member1.pk],
            )
        )

        self.assertFalse(TeamMember.objects.filter(pk=self.member1.pk).exists())

        self.assertRedirects(
            response,
            reverse("accounts:team_member_list"),
        )

    def test_user_cannot_delete_another_users_team_member(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse(
                "accounts:team_member_delete",
                args=[self.member2.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        self.assertTrue(TeamMember.objects.filter(pk=self.member2.pk).exists())
