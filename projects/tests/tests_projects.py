from django.shortcuts import reverse

from custom.tests import TestBase, BasicTestsMixin
from ..models import Project, Member


class ProjectTestBase(TestBase):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            name='Test Project',
            color='#0000ff',
            owner=self.user1,
        )
        self.project.save()

        self.project.members.add(Member.objects.create(
            user=self.user1,
            project=self.project,
            role=3,
        ))


class ProjectCreateTest(ProjectTestBase):
    def setUp(self):
        super().setUp()
        self.project.members.add(Member.objects.create(
            user=self.user2,
            project=self.project,
            role=2,
        ))

    def test_slug(self):
        self.assertEqual(self.project.slug, 'test-project')

    def test_users(self):
        project_users = self.project.users
        self.assertTrue(self.user1 in project_users)
        self.assertTrue(self.user2 in project_users)
        self.assertEqual(len(project_users), 2)

    def test_get_absolute_url(self):
        self.assertEqual(self.project.get_absolute_url(), f'/project/{self.project.slug}/')


class ProjectCreateViewTest(BasicTestsMixin, TestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = '/create'
        self.desired_reverse_url = reverse('project_create')
        self.desired_template = 'projects/project_create.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_POST_create_project(self):
        resp = self.client.post(self.desired_reverse_url, {
            'name': 'Raindeeeers',
            'color': '#ffaa00'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/project/raindeeeers/')

        project = Project.objects.get(name='Raindeeeers')
        self.assertTrue(self.user1 in project.users)
        self.assertEqual(len(project.users), 1)
        self.assertTrue(Member.objects.filter(user=self.user1, project=project).exists())


class ProjectDetailsViewTest(BasicTestsMixin, ProjectTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/'
        self.desired_reverse_url = reverse('project_details', args=[self.project.slug])
        self.desired_template = 'projects/project_details.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_member_access(self):
        self.client.force_login(self.user2)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)


class ProjectSettingsViewTest(BasicTestsMixin, ProjectTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/settings'
        self.desired_reverse_url = reverse('project_settings', args=[self.project.slug])
        self.desired_template = 'projects/project_settings.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_owner_access(self):
        self.client.force_login(self.user2)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_new_settings(self):
        resp = self.client.post(self.desired_reverse_url, {
            'name': 'Test Porojecto',
            'color': '#ffff00'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f'/project/{self.project.slug}/')

        project = Project.objects.first()
        self.assertEqual(self.project.id, project.id)
        self.assertEqual(project.name, 'Test Porojecto')
        self.assertEqual(project.color, '#ffff00')

    def test_non_owner_post_new_settings(self):
        self.client.force_login(self.user2)
        resp = self.client.post(self.desired_reverse_url, {
            'name': 'Test Porojecto',
            'color': '#ffff00'
        })
        self.assertEqual(resp.status_code, 403)


class ProjectDeleteViewTest(BasicTestsMixin, ProjectTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/delete'
        self.desired_reverse_url = reverse('project_delete', args=[self.project.slug])
        self.desired_template = 'projects/project_delete.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_owner_access(self):
        self.client.force_login(self.user2)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_delete_project(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')

        project = Project.objects.first()
        self.assertIsNone(project)

    def test_non_owner_post_delete_project(self):
        self.client.force_login(self.user2)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)


class ProjectLeaveViewTest(BasicTestsMixin, ProjectTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/leave'
        self.desired_reverse_url = reverse('project_leave', args=[self.project.slug])
        self.desired_template = 'projects/project_leave.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

        self.project.members.add(Member.objects.create(
            user=self.user2,
            project=self.project,
            role=2
        ))
        self.client.force_login(self.user2)

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_inaccessible_by_owner(self):
        self.client.force_login(self.user1)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_project_leave(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/')
        self.assertIsNone(self.user2.projects.first())
