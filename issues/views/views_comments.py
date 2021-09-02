from django.views.generic import DetailView
from django.shortcuts import HttpResponseRedirect, get_object_or_404, HttpResponse

from issues.forms import CommentCreateForm
from issues.models import Comment, Issue
from projects.models import Member
from custom.mixins import HierarchicalSlugMixin, MemberIsDeveloperOrOwnerMixin


class CommentCreateView(HierarchicalSlugMixin, MemberIsDeveloperOrOwnerMixin, DetailView):
    model = Issue

    def post(self, request, *args, **kwargs):
        member = get_object_or_404(Member, project__slug=self.kwargs.get('project_slug'), user=request.user)
        if member.role < 2:
            return HttpResponse(status=403)
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = Comment(**form.cleaned_data)
            comment.author = request.user
            comment.issue = self.get_object()
            comment.save()
        return HttpResponseRedirect(comment.issue.get_absolute_url())


class CommentDeleteView(HierarchicalSlugMixin, MemberIsDeveloperOrOwnerMixin, DetailView):
    model = Issue  # Same case as in MemberDetailsView

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, issue=self.get_object(), id=self.kwargs.get('comment_id'))
        member = get_object_or_404(Member, project__slug=self.kwargs.get('project_slug'), user=request.user)
        if not member.is_owner and member.role != 3 and request.user != comment.author:
            return HttpResponse(status=403)
        comment.delete()
        return HttpResponseRedirect(comment.issue.get_absolute_url())