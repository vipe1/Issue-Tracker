from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404, Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from custom.mixins import HierarchicalSlugMixin, ProjectSidebarLinks, UserInProjectMixin
from projects.models import Project, Member
from ..tables import UserTable


class ProjectMemberListView(ProjectSidebarLinks, SingleTableMixin, UserInProjectMixin, TemplateView):
    template_name = 'projects/members/members_list.html'
    table_class = UserTable

    def get_table_data(self):
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        return Member.objects.filter(project=project)  # I could do it in one line but it would be barely readable


class MemberDetailsView(ProjectSidebarLinks, HierarchicalSlugMixin, UserInProjectMixin, DetailView):
    """
    'model = Project' may be confusing but it's actually what makes this view work properly.
    Basically, if we would get 'model = Member' the 'project_slug' wouldn't matter
    and every Member could be seen no matter which 'project_slug' is used.

    'model = Project' and 'get_object' method extension make sure that
    the Member is actually seen only from proper 'project_slug'.
    """
    model = Project
    template_name = 'projects/members/member_details.html'

    def get_object(self, queryset=None):
        project = super(MemberDetailsView, self).get_object()
        member = project.members.filter(id=self.kwargs.get('member_id')).first()
        if member is None:
            raise Http404
        return member

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        user_member = get_object_or_404(
            Member,
            user=request.user,
            project=project,
        )
        member = get_object_or_404(
            Member,
            project=project,
            id=self.kwargs.get('member_id')
        )

        roles = {
            'admin': 3,
            'developer': 2,
            'spectator': 1,
        }
        role = roles.get(request.POST.get('new_role'))
        if role not in (1, 2, 3):
            return HttpResponse(status=400)

        if user_member == member:  # Prevent member from trying to give role to himself
            return HttpResponse(status=403)
        if request.user != project.owner:  # If user is not project owner
            if user_member.role != 3 or member.role == 3 or role == 3:
                # Not-admins cannot give roles | Cannot change role of admin | Cannot give admin role
                return HttpResponse(status=403)

        member.role = role
        member.save()
        return HttpResponseRedirect(member.get_absolute_url())


class MemberKickView(ProjectSidebarLinks, HierarchicalSlugMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'projects/members/member_kick.html'

    def get_object(self, queryset=None):
        project = super(MemberKickView, self).get_object()
        member = project.members.filter(id=self.kwargs.get('member_id')).first()
        if member is None:
            raise Http404
        return member

    def post(self, request, *args, **kwargs):
        member = self.get_object()
        member.delete()
        return HttpResponseRedirect(reverse_lazy('project_members', args=[member.project.slug]))

    def test_func(self):
        return self.request.user == self.get_object().project.owner and not self.get_object().is_owner