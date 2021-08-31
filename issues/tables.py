from django_tables2 import tables
from django.utils.html import format_html
from django.apps import apps

from issues.models import Comment


class CommentTable(tables.Table):
    delete = tables.columns.TemplateColumn(template_name='django_tables2/comment_delete_column.html')

    class Meta:
        model = Comment
        exclude = ('id', 'issue')
        order_by = '-created_at'


class HistoryTable(tables.Table):
    field = tables.columns.Column()
    old_value = tables.columns.Column()
    new_value = tables.columns.Column()

    def render_field(self, value):
        return value.title()

    def render_old_value(self, value, record):
        return format_html(parse_history_value(value, record['field']))

    def render_new_value(self, value, record):
        return format_html(parse_history_value(value, record['field']))


def parse_history_value(value, field):
    if field in ('name', 'description'):
        return value
    elif field == 'assignee':
        user = apps.get_model('users.CustomUser').objects.filter(id=value).first()
        if user is not None:
            return user.get_full_name()
        return '—'
    elif field in ('type', 'priority', 'status'):
        return value.title().replace('_', ' ')
    return value
