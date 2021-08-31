from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, View, TemplateView
from django.contrib import messages
from django_tables2 import SingleTableMixin

from custom.mixins import ProjectSidebarLinks, MemberIsAdminOrOwnerMixin
from projects.models import Project, ProjectInvitation, Member
from ..tables import InvitationTable


class ProjectInviteView(LoginRequiredMixin, DetailView):
    model = ProjectInvitation
    context_object_name = 'invitation'

    def post(self, request, slug, *args, **kwargs):
        content = request.POST
        invitation = ProjectInvitation.objects.get(slug=slug)
        project = invitation.project
        if 'button_accepted' in content:
            invitation.status = 'accepted'
            Member.objects.create(
                user=request.user,
                project=project,
            )
        elif 'button_declined' in content:
            invitation.status = 'declined'
        else:
            return HttpResponseBadRequest
        invitation.save()
        return redirect('dashboard')

    def get_template_names(self):
        status = self.object.status
        if status == 'active':
            return ['projects/project_invite_active.html']
        return ['projects/project_invite_inactive.html']


class ProjectInviteGeneratorView(MemberIsAdminOrOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        if len(project.invites.filter(status='active')) >= 5:
            messages.error(request, 'You can have max. 5 active invites per project')
            return HttpResponseRedirect(reverse_lazy('project_invite_list', args=[project.slug]))


        invitation = ProjectInvitation(project=project)
        invitation.save()

        messages.success(request, invitation.get_absolute_url())
        return HttpResponseRedirect(reverse_lazy('project_invite_list', args=[project.slug]))


class ProjectInviteListView(ProjectSidebarLinks, SingleTableMixin, MemberIsAdminOrOwnerMixin, TemplateView):
    template_name = 'projects/project_invite_list.html'
    table_class = InvitationTable

    def get_table_data(self):
        return get_object_or_404(Project, slug=self.kwargs.get('project_slug')).invites.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        return context


class ProjectInviteDeleteView(MemberIsAdminOrOwnerMixin, View):
    def post(self, request, **kwargs):
        invitation = get_object_or_404(
            ProjectInvitation,
            project__slug=kwargs.get('project_slug'),
            id=kwargs.get('invite_id')
        )
        invitation.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))