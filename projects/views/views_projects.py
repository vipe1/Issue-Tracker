from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, HttpResponse, HttpResponseRedirect

from custom.mixins import HierarchicalSlugMixin, UserInProjectMixin, ProjectSidebarLinks, UserIsOwnerMixin
from projects.forms import ProjectCreateForm
from projects.models import Project, Member


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectCreateForm
    template_name = 'projects/project_create.html'

    def get_form_kwargs(self):
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('project_details', args=[self.object.slug])


class ProjectDetailsView(ProjectSidebarLinks, HierarchicalSlugMixin, UserInProjectMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sort_by'] = self.request.GET.get('sort')
        return context


class ProjectSettingsView(ProjectSidebarLinks, HierarchicalSlugMixin, UserIsOwnerMixin, UpdateView):
    model = Project
    template_name = 'projects/project_settings.html'
    fields = ('name', 'color')

    def get_success_url(self):
        return reverse_lazy('project_details', args=[self.object.slug])


class ProjectDeleteView(ProjectSidebarLinks, HierarchicalSlugMixin, UserIsOwnerMixin, DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class ProjectLeaveView(ProjectSidebarLinks, UserPassesTestMixin, TemplateView):
    template_name = 'projects/project_leave.html'

    def post(self, request, **kwargs):
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        if request.user == project.owner:
            return HttpResponse(status=403)
        member = get_object_or_404(Member, project=project, user=request.user)
        member.delete()
        return HttpResponseRedirect(reverse_lazy('dashboard'))

    def test_func(self):
        project = get_object_or_404(Project, slug=self.kwargs.get('project_slug'))
        return self.request.user in project.users and self.request.user != project.owner
