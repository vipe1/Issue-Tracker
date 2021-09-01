from django.test import TestCase
from django.contrib.auth import get_user_model


class TestBase(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='peter_r0ck',
            first_name='Peter',
            last_name='Rock',
            email='peterrock@test.com',
            password='petroR12399'
        )
        self.client.login(username='peter_r0ck', password='petroR12399')

        self.user2 = get_user_model().objects.create(
            username='john_doe90',
            first_name='John',
            last_name='Doe',
            email='johndoedee@test.com',
            password='brrr92kks'
        )

class BasicTestsMixin:
    """
    Basic repetitive tests:
        - Is view accessible at particular url
        - Is view accessible at particular reverse url
        - Is view using correct template
    """
    def test_accessible_by_url(self):
        resp = self.client.get(self.desired_manual_url)
        self.assertEqual(resp.status_code, 200)

    def test_accessible_by_reverse_name(self):
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 200)

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_correct_template_used(self):
        resp = self.client.get(self.desired_reverse_url)
        self.assertTemplateUsed(resp, self.desired_template)