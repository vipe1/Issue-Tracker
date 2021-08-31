from django.urls import path, include

from .views import IssueDetailView, IssueEditView, IssueDeleteView, IssueSetStatusView, IssueCreateView,\
    CommentCreateView, CommentDeleteView

urlpatterns = [
    path('issue-create', IssueCreateView.as_view(), name='issue_create'),

    path('<slug:issue_slug>/', include([
        path('', IssueDetailView.as_view(), name='issue_detail'),
        path('edit', IssueEditView.as_view(), name='issue_edit'),
        path('delete', IssueDeleteView.as_view(), name='issue_delete'),
        path('set-status', IssueSetStatusView.as_view(), name='issue_set_status'),

        path('comments/', include([
            path('', CommentCreateView.as_view(), name='comment_create'),
            path('<int:comment_id>/delete', CommentDeleteView.as_view(), name='comment_delete')
        ]))
    ])),
]
