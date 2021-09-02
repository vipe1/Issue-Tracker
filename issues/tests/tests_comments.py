from django.urls import reverse

from .tests_issues import IssuesTestBase
from ..models import Comment


class CommentsTestBase(IssuesTestBase):
    def setUp(self):
        super().setUp()
        self.comment1 = Comment.objects.create(
            issue=self.issue1,
            author=self.user1,
            content='Test comment'
        )


class CommentCreateViewTest(CommentsTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/comments/'
        self.desired_reverse_url = reverse('comment_create', args=[self.project.slug, self.issue1.slug])
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url
        self.start_url = self.issue1.get_absolute_url()
        self.comment_content = {
            'content': 'Test comment content'
        }

    def test_accessible_by_url(self):
        resp = self.client.post(self.desired_manual_url, self.comment_content, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_accessible_by_reverse_name(self):
        resp = self.client.post(self.desired_reverse_url, self.comment_content, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_POST_comment_create(self):
        resp = self.client.post(self.desired_reverse_url, self.comment_content, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)
        self.assertIsNotNone(Comment.objects.filter(author=self.user1, content='Test comment content').first())

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url, self.comment_content, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 404)

    def test_POST_spectator(self):
        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url, self.comment_content, HTTP_REFERER=self.start_url)
        self.assertEqual(resp.status_code, 403)


class CommentDeleteViewTest(CommentsTestBase):
    def setUp(self):
        super().setUp()
        self.desired_manual_url = f'/project/{self.project.slug}/i/{self.issue1.slug}/comments/{self.comment1.id}/delete'
        self.desired_reverse_url = reverse('comment_delete', args=[self.project.slug, self.issue1.slug, self.comment1.id])
        self.expected_redirect_url = '/login/?next=' + self.desired_manual_url
        self.start_url = self.issue1.get_absolute_url()

    def test_accessible_by_url(self):
        resp = self.client.post(self.desired_manual_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_accessible_by_reverse_name(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)

    def test_manual_and_reverse_name_url_are_same(self):
        self.assertEqual(self.desired_manual_url, self.desired_reverse_url)

    def test_POST_comment_delete(self):
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.start_url)
        self.assertIsNone(Comment.objects.filter(id=self.comment1.id).first())

    def test_POST_non_member(self):
        self.client.force_login(self.user6)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 404)

    def test_POST_spectator(self):
        self.client.force_login(self.user5)
        resp = self.client.post(self.desired_reverse_url)
        self.assertEqual(resp.status_code, 403)