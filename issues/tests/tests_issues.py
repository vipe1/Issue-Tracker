from django.urls import reverse

from projects.tests.tests_members import MembersTestBase
from ..models import Issue
from custom.tests import BasicTestsMixin


class IssuesTestBase(MembersTestBase):
    def setUp(self):
        super().setUp()
        self.issue1 = Issue.objects.create(
            name='Typo on main page',
            description='Navbar home button has typo',
            type='task',
            project=self.project,
            author=self.user4,
        )


class IssueDetailsViewTest(BasicTestsMixin, IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/'
        self.desired_reverse_url = reverse('issue_details', args=[self.project.slug, self.issue1.slug])
        self.desired_template = 'issues/issue_details.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_member_access(self):
        self.client.force_login(self.user6)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)


class IssueCreateViewTest(BasicTestsMixin, IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/issue-create'
        self.desired_reverse_url = reverse('issue_create', args=[self.project.slug])
        self.desired_template = 'issues/issue_create.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url
        self.dummy_data = {
            'name': 'Test issue',
            'description': 'Test description',
            'type': 'new_feature',
            'priority': 'low',
        }

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_member_access(self):
        self.client.force_login(self.user6)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 404)

    def test_spectator_access(self):
        self.client.force_login(self.user5)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_create_issue(self):
        resp = self.client.post(self.desired_reverse_url, self.dummy_data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.project.get_absolute_url())

        issue = Issue.objects.filter(name='Test issue', type='new_feature').first()
        self.assertIsNotNone(issue)

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url, self.dummy_data)
        self.assertEqual(resp.status_code, 404)

    def test_POST_spectator(self):
        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url, self.dummy_data)
        self.assertEqual(resp.status_code, 403)


class IssueEditViewTest(BasicTestsMixin, IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/edit'
        self.desired_reverse_url = reverse('issue_edit', args=[self.project.slug, self.issue1.slug])
        self.desired_template = 'issues/issue_edit.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url
        self.dummy_data = {
            'name': 'Test issue edit',
            'description': 'Test description changed',
            'type': 'task',
            'priority': 'highest',
        }

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_member_access(self):
        self.client.force_login(self.user6)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 404)

    def test_spectator_access(self):
        self.client.force_login(self.user5)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_issue_edit(self):
        resp = self.client.post(self.desired_reverse_url, self.dummy_data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('issue_details', args=[self.project.slug, self.issue1.slug]))
        self.assertIsNotNone(Issue.objects.filter(**self.dummy_data).first())

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url, self.dummy_data)
        self.assertEqual(resp.status_code, 404)

    def test_POST_spectator(self):
        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url, self.dummy_data)
        self.assertEqual(resp.status_code, 403)


class IssueDeleteViewTest(BasicTestsMixin, IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/delete'
        self.desired_reverse_url = reverse('issue_delete', args=[self.project.slug, self.issue1.slug])
        self.desired_template = 'issues/issue_delete.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_member_access(self):
        self.client.force_login(self.user6)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 404)

    def test_spectator_access(self):
        self.client.force_login(self.user5)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_issue_delete(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_details', args=[self.project.slug]))
        self.assertIsNone(Issue.objects.filter(id=self.issue1.id).first())

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 404)

    def test_POST_spectator(self):
        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)


class IssueSetStatusViewTest(IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/set-status'
        self.desired_reverse_url = reverse('issue_set_status', args=[self.project.slug, self.issue1.slug])
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url
        self.start_url = self.project.get_absolute_url()
        self.new_status = {
            'new_status': 'closed'
        }

    def test_accessible_by_url(self):
        resp = self.client.post(self.desired_manual_url, self.new_status, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_accessible_by_reverse_name(self):
        resp = self.client.post(self.desired_reverse_url, self.new_status, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_POST_issue_set_status(self):
        resp = self.client.post(self.desired_reverse_url, self.new_status, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)
        self.assertEqual(Issue.objects.get(id=self.issue1.id).status, 'closed')

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url, self.new_status, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 404)

    def test_POST_spectator(self):
        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url, self.new_status, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_assigned_issue(self):
        self.assertIsNone(Issue.objects.get(id=self.issue1.id).assignee)

        resp = self.client.post(self.desired_reverse_url, {'new_status': 'in_progress'}, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)
        self.assertEqual(Issue.objects.get(id=self.issue1.id).assignee, self.user1)
        self.assertEqual(Issue.objects.get(id=self.issue1.id).status, 'in_progress')

        self.client.force_login(self.user4)
        resp = self.client.post(self.desired_reverse_url, {'new_status': 'closed'}, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 403)

        self.client.force_login(self.user3)
        resp = self.client.post(self.desired_reverse_url, {'new_status': 'closed'}, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)


class IssueAssignUserViewTest(IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/assign-user'
        self.desired_reverse_url = reverse('issue_assign_user', args=[self.project.slug, self.issue1.slug])
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url
        self.start_url = self.project.get_absolute_url()
        self.new_assignee = {
            'new_assignee': self.user4.id
        }
        self.client.force_login(self.user3)

    def test_accessible_by_url(self):
        resp = self.client.post(self.desired_manual_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_accessible_by_reverse_name(self):
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_POST_issue_assign_user(self):
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)
        self.assertEqual(Issue.objects.get(id=self.issue1.id).assignee, self.user4)

    def test_POST_bad_request(self):
        resp = self.client.post(self.desired_reverse_url, {'new_assignee': self.user6.id}, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post(self.desired_reverse_url, {'new_assignee': self.user5.id}, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 400)

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 404)

    def test_POST_unauthorized_member(self):
        self.client.force_login(self.user4)
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 403)

        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_assigned_issue(self):
        self.assertIsNone(Issue.objects.get(id=self.issue1.id).assignee)

        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)
        self.assertEqual(Issue.objects.get(id=self.issue1.id).assignee, self.user4)
        self.assertEqual(Issue.objects.get(id=self.issue1.id).status, 'in_progress')

        self.client.force_login(self.user4)
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 403)

        self.client.force_login(self.user3)
        resp = self.client.post(self.desired_reverse_url, self.new_assignee, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)