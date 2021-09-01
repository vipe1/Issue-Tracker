from django.test import SimpleTestCase
from django.shortcuts import reverse

from .models import CustomUser
from custom.tests import TestBase, BasicTestsMixin


# Create your tests here.
class CreatedUsersTest(TestBase):
    def test_users_use_correct_model(self):
        self.assertIsInstance(self.user1, CustomUser)
        self.assertIsInstance(self.user2, CustomUser)


class SignupViewTest(BasicTestsMixin, SimpleTestCase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = '/signup/'
        self.desired_reverse_url = reverse('signup')
        self.desired_template = 'registration/signup.html'


class AccountSettingsViewTest(BasicTestsMixin, TestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = '/account-settings/'
        self.desired_reverse_url = reverse('account_settings')
        self.desired_template = 'accounts/account_settings.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)
