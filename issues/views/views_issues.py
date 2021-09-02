from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from django_tables2 import MultiTableMixin

from custom.mixins import HierarchicalSlugMixin, UserInProjectMixin, ProjectSidebarLinks, \
    MemberIsDeveloperOrOwnerMixin, MemberCanControlIssue
from issues.models import Issue
from issues.forms import IssueCreateEditForm, CommentCreateForm
from projects.models import Project, Member
from ..tables import CommentTable, HistoryTable


class IssueDetailsView(ProjectSidebarLinks, MultiTableMixin, HierarchicalSlugMixin, UserInProjectMixin, DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issues/issue_details.html'

    def get_comments(self):
        return CommentTable(self.get_object().comments.all())

    def get_history(self):
        data = []
        changes = list(self.get_object().history.all())
        if len(changes) > 1:
            for idx, old_record in enumerate(changes[:-1]):
                new_record = changes[idx + 1]
                delta = new_record.diff_against(old_record)
                for change in delta.changes:
                    data.append({
                        'field': change.field,
                        'old_value': change.new,
                        'new_value': change.old,
                    })
        return HistoryTable(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        self.tables = [
            self.get_comments(),
            self.get_history()
        ]
        return super(IssueDetailsView, self).dispatch(request, *args, **kwargs)


class IssueCreateView(ProjectSidebarLinks, HierarchicalSlugMixin, MemberIsDeveloperOrOwnerMixin, CreateView):
    form_class = IssueCreateEditForm
    template_name = 'issues/issue_create.html'

    def post(self, request, *args, **kwargs):
        form = IssueCreateEditForm(request.POST)
        if not form.is_valid():
            print(form.cleaned_data)
            return HttpResponse(status=400)

        project_slug = kwargs.get('project_slug')
        project = get_object_or_404(
            Project,
            slug=project_slug
        )

        member = get_object_or_404(Member, project=project, user=request.user)
        if member.role < 2:
            return HttpResponse(status=403)

        issue = Issue(**form.cleaned_data)
        issue.author = request.user
        issue.project = project
        issue.save()

        return redirect('project_details', project_slug)


class IssueEditView(ProjectSidebarLinks, HierarchicalSlugMixin, MemberCanControlIssue, UpdateView):
    model = Issue
    form_class = IssueCreateEditForm
    template_name = 'issues/issue_edit.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class IssueDeleteView(ProjectSidebarLinks, HierarchicalSlugMixin, MemberCanControlIssue, DeleteView):
    model = Issue
    template_name = 'issues/issue_delete.html'

    def get_success_url(self):
        return self.object.project.get_absolute_url()


class IssueSetStatusView(MemberIsDeveloperOrOwnerMixin, View):
    ISSUE_STATUSES_VALUES = (
        'open',
        'reopened',
        'in_progress',
        'resolved',
        'closed',
    )

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs.get('project_slug'))
        member = get_object_or_404(Member, project=project, user=request.user)
        issue = get_object_or_404(
            Issue,
            project=project,
            slug=kwargs.get('issue_slug')
        )
        new_status = request.POST['new_status']

        if issue.status == 'in_progress' and request.user != issue.assignee \
                and not (member.is_owner or member.role == 3):
            return HttpResponse(status=403)
        if new_status not in self.ISSUE_STATUSES_VALUES:
            return HttpResponse(status=400)

        issue.status = new_status
        if new_status == 'in_progress':
            issue.assignee = request.user
        elif new_status in ('open', 'reopened'):
            issue.assignee = None
        issue.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
