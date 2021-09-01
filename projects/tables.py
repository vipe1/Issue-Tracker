from django_tables2 import tables, A

from .models import Member, ProjectInvitation


class UserTable(tables.Table):
    details = tables.columns.LinkColumn(
        'member_details',
        args=[A('project.slug'), A('pk')],
        text='Details'
    )

    class Meta:
        model = Member
        fields = ('id', 'user', 'joined_at', 'role')
        order_by = '-role'

    def render_role(self, value, record):
        if record.is_owner:
            return 'Owner'
        return value


class InvitationTable(tables.Table):
    delete = tables.columns.TemplateColumn(template_name='django_tables2/invite_delete_column.html')

    class Meta:
        model = ProjectInvitation
        fields = ('slug', 'status')
        order_by = '-status'