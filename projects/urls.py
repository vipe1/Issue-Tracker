from django.urls import path, include

from .views import ProjectDetailsView, ProjectCreateView, ProjectSettingsView, ProjectDeleteView, ProjectInviteView, \
    ProjectInviteGeneratorView, ProjectMemberListView, MemberDetailsView, MemberKickView, ProjectInviteListView, \
    ProjectInviteDeleteView, ProjectLeaveView

urlpatterns = [
    path('create', ProjectCreateView.as_view(), name='project_create'),
    path('project/', include([
        path('invite/<slug:slug>', ProjectInviteView.as_view(), name='project_invite'),


        path('<slug:project_slug>/', include([
            path('', ProjectDetailsView.as_view(), name='project_details'),
            path('settings', ProjectSettingsView.as_view(), name='project_settings'),
            path('delete', ProjectDeleteView.as_view(), name='project_delete'),
            path('leave', ProjectLeaveView.as_view(), name='project_leave'),

            path('invites/', include([
                path('', ProjectInviteListView.as_view(), name='project_invite_list'),
                path('generate', ProjectInviteGeneratorView.as_view(), name='project_invite_generator'),
                path('<int:invite_id>/delete', ProjectInviteDeleteView.as_view(), name='project_invite_delete')
            ])),


            path('members/', include([
                path('', ProjectMemberListView.as_view(), name='project_members'),
                path('<int:member_id>/', include([
                    path('', MemberDetailsView.as_view(), name='member_details'),
                    path('kick', MemberKickView.as_view(), name='member_kick'),
                ])),
            ])),


            path('i/', include('issues.urls')),
        ])),
    ]))
]
