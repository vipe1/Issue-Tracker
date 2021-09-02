from django.urls import reverse

from .tests_members import MembersTestBase
from custom.tests import BasicTestsMixin
from ..models import ProjectInvitation


class InvitesTestBase(MembersTestBase):
    def setUp(self):
        super().setUp()
        self.invite1 = ProjectInvitation.objects.create(project=self.project)
        self.invite2 = ProjectInvitation.objects.create(project=self.project, status='accepted')
        self.invite3 = ProjectInvitation.objects.create(project=self.project, status='declined')


class ProjectInviteViewTest(InvitesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/invite/{self.invite1.slug}'
        self.desired_reverse_url = reverse('project_invite', args=[self.invite1.slug])
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_accessible_by_url(self):
        resp = self.client.get(self.desired_manual_url)
        self.assertEqual(resp.status_code, 200)

    def test_accessible_by_reverse_name(self):
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 200)

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_correct_template_used(self):
        resp = self.client.get(reverse('project_invite', args=[self.invite1.slug]))
        self.assertTemplateUsed(resp, 'projects/invites/project_invite_active.html')

        resp = self.client.get(reverse('project_invite', args=[self.invite2.slug]))
        self.assertTemplateUsed(resp, 'projects/invites/project_invite_inactive.html')

        resp = self.client.get(reverse('project_invite', args=[self.invite3.slug]))
        self.assertTemplateUsed(resp, 'projects/invites/project_invite_inactive.html')

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)


class ProjectInviteListViewTest(BasicTestsMixin, InvitesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/invites/'
        self.desired_reverse_url = reverse('project_invite_list', args=[self.project.slug])
        self.desired_template = 'projects/invites/project_invite_list.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)


class ProjectInviteGeneratorViewTest(InvitesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/invites/generate'
        self.desired_reverse_url = reverse('project_invite_generator', args=[self.project.slug])

    def test_accessible_by_url(self):
        resp = self.client.post(self.desired_manual_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))

    def test_accessible_by_reverse_name(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_POST_generate_invite(self):
        counter_active_issues = len(self.project.invites.filter(status='active'))
        for i in range(4):  # Because I've already created 3 before, but 2 are inactive
            resp = self.client.post(self.desired_reverse_url)
            self.assertEqual(resp.status_code, 302)
            self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))
            counter_active_issues += 1
            self.assertEqual(counter_active_issues, len(self.project.invites.filter(status='active')))

        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))
        self.assertEqual(len(self.project.invites.filter(status='active')), 5)

    def test_POST_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=' + self.desired_manual_url)

    def test_POST_by_non_authorized_member(self):
        self.client.force_login(self.user4)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)


class ProjectInviteDeleteViewTest(InvitesTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/invites/{self.invite1.id}/delete'
        self.desired_reverse_url = reverse('project_invite_delete', args=[self.project.slug, self.invite1.id])

    def test_accessible_by_url(self):
        resp = self.client.post(self.desired_manual_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))

    def test_accessible_by_reverse_name(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_POST_generate_invite(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('project_invite_list', args=[self.project.slug]))

    def test_POST_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/login/?next=' + self.desired_manual_url)

    def test_POST_by_non_authorized_member(self):
        self.client.force_login(self.user4)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)
