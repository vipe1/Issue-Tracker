from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import Http404, get_object_or_404
from django.utils.translation import gettext as _
from projects.models import Project, Member


class HierarchicalSlugMixin:
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        project_slug = self.kwargs.get('project_slug')
        issue_slug = self.kwargs.get('issue_slug')

        if project_slug is not None:
            if issue_slug is not None:
                queryset = queryset.filter(
                    project__slug=project_slug,
                    slug=issue_slug
                )
            else:
                queryset = queryset.filter(
                    slug=project_slug
                )
        else:
            raise AttributeError(
                f'Generic detail view {self.__class__.__name__} must be called with either an object '
                'pk or a slug in the URLconf.'
                'Slightly modified it so only I know how to really use it :PepeLaugh:'
            )
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_(f'No {queryset.model._meta.verbose_name}s found matching the query'))
        return obj


class UserInProjectMixin(UserPassesTestMixin):
    def test_func(self):
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        return self.request.user in project.users


class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().owner


class ProjectSidebarLinks:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        context['project_slug'] = project.slug
        context['project_name'] = project.name
        context['project_owner'] = project.owner
        context['user_member'] = get_object_or_404(
            Member, project=project, user=self.request.user
        )
        return context


class MemberIsAdminOrOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        member = get_object_or_404(Member, project__slug=self.kwargs.get('project_slug'), user=self.request.user)
        return member.is_owner or member.role == 3


class MemberIsDeveloperOrOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        member = get_object_or_404(Member, project__slug=self.kwargs.get('project_slug'), user=self.request.user)
        return member.is_owner or member.role > 1


class MemberCanControlIssueMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        member = get_object_or_404(Member, project__slug=self.kwargs.get('project_slug'), user=self.request.user)
        return member.is_owner or member.role == 3 or self.get_object().author == self.request.user