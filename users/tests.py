from django.test import SimpleTestCase
from django.shortcuts import reverse

from .models import CustomUser
from custom.tests import TestBase, BasicTestsMixin


# Create your tests here.
class CreatedUsersTest(TestBase):
    def test_users_use_correct_model(self):
        self.assertIsInstance(self.user1, CustomUser)
        self.assertIsInstance(self.user2, CustomUser)


class SignupViewTest(BasicTestsMixin, TestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = '/signup/'
        self.desired_reverse_url = reverse('signup')
        self.desired_template = 'registration/signup.html'

    def test_POST_signup(self):
        # It should fail because of implemented reCAPTCHA
        resp = self.client.post(self.desired_reverse_url, {
            'username': 'barrybbenson',
            'email': 'barrybbenson@test.com',
            'first_name': 'Barry',
            'last_name': 'Benson',
            'password': '20un93fr4hj',
            'password2': '20un93fr4hj',
        })
        self.assertEqual(resp.status_code, 200)

        user = CustomUser.objects.filter(username='barrybbenson', email='barrybbenson@test.com')
        self.assertFalse(user.exists())


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

    def test_POST_account_settings_change(self):
        resp = self.client.post(self.desired_reverse_url, {
            'username': 'BennyJaxon',
            'email': 'bjaxon@test.com'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.desired_reverse_url)

        user = CustomUser.objects.get(id=self.user1.id)
        self.assertEqual(user.username, 'BennyJaxon')
        self.assertEqual(user.email, 'bjaxon@test.com')


class LoginViewTest(TestBase):
    def test_POST_login(self):
        self.client.logout()

        resp = self.client.get(reverse('account_settings'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=/account-settings/')

        resp = self.client.post(reverse('login'), {
            'username': 'peter_r0ck',
            'password': 'petroR12399'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('dashboard'))

        resp = self.client.get(reverse('account_settings'))
        self.assertEqual(resp.status_code, 200)