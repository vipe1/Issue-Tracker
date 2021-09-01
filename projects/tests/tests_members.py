from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from custom.tests import BasicTestsMixin
from ..models import Project, Member
from .tests_projects import ProjectTestBase


class MembersTestBase(ProjectTestBase):
    def setUp(self):
        super().setUp()
        self.user3 = get_user_model().objects.create(
            username='joe_butcher',
            first_name='Joe',
            last_name='Butcher',
            email='joebutchee@test.com',
            password='jm0eds4rhj'
        )
        self.user4 = get_user_model().objects.create(
            username='denzel_cansas',
            first_name='Denzel',
            last_name='Cansas',
            email='denzel_cansas_@test.com',
            password='hj9082g4mn7'
        )
        self.user5 = get_user_model().objects.create(
            username='mark_russell',
            first_name='Mark',
            last_name='Russell',
            email='markrussselll@test.com',
            password='23uj1x234e8'
        )
        self.user6 = get_user_model().objects.create(
            username='gregy0rk',
            first_name='Greg',
            last_name='York',
            email='gr3gyork@test.com',
            password='2h0438szj3'
        )

        def create_member(user, role):
            Member.objects.create(
                user=user,
                project=self.project,
                role=role
            )

        create_member(self.user2, 3)
        create_member(self.user3, 3)
        create_member(self.user4, 2)
        create_member(self.user5, 1)


class ProjectMemberListViewTest(BasicTestsMixin, MembersTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/members/'
        self.desired_reverse_url = reverse('project_members', args=[self.project.slug])
        self.desired_template = 'projects/members/members_list.html'
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


class ProjectMemberDetailsViewTest(BasicTestsMixin, MembersTestBase):
    def setUp(self):
        super().setUp()
        self.member = Member.objects.filter(project=self.project, user=self.user2).first()
        self.desired_manual_url = f'/project/{self.project.slug}/members/{self.member.id}/'
        self.desired_reverse_url = reverse('member_details', args=[self.project.slug, self.member.id])
        self.desired_template = 'projects/members/member_details.html'
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url

    def test_access_from_different_project(self):
        decoy_project = Project.objects.create(
            name='Decoy Project',
            color='#00000',
            owner=self.user6
        )
        resp = self.client.get(reverse('member_details', args=[decoy_project.slug, self.member.id]))
        self.assertEqual(resp.status_code, 403)

        decoy_project.members.add(Member.objects.create(
            user=self.user1,
            project=decoy_project,
            role=3
        ))
        resp = self.client.get(reverse('member_details', args=[decoy_project.slug, self.member.id]))
        self.assertEqual(resp.status_code, 404)

    def test_inaccessible_by_non_logged_user(self):
        self.client.logout()
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.expected_redirect_url)

    def test_non_member_access(self):
        self.client.force_login(self.user6)
        resp = self.client.get(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)

    def test_POST_set_role(self):
        member = Member.objects.filter(project=self.project, role=1).first()
        resp = self.client.post(member.get_absolute_url(), {'new_role': 'developer'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, member.get_absolute_url())
        self.assertEqual(Member.objects.get(id=member.id).role, 2)

    def test_POST_unauthorized_member_set_role(self):
        # Despite it's weird look this test is actually pretty fast

        for user in (self.user5, self.user4):
            self.client.force_login(user)
            for member in self.project.members.all():
                for role in ('spectator', 'developer', 'admin'):
                    resp = self.client.post(member.get_absolute_url(), {'new_role': role})
                    self.assertEqual(resp.status_code, 403)

        for user in (self.user2, self.user3):
            self.client.force_login(user)
            for role in ('spectator', 'developer', 'admin'):
                for member in self.project.members.filter(Q(role=3) | Q(user=self.project.owner)):
                    resp = self.client.post(member.get_absolute_url(), {'new_role': role})
                    self.assertEqual(resp.status_code, 403)

        self.client.force_login(self.user1)
        member = self.project.members.get(user=self.user1)
        for role in ('spectator', 'developer', 'admin'):
            resp = self.client.post(member.get_absolute_url(), {'new_role': role})
            self.assertEqual(resp.status_code, 403)
