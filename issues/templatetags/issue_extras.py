from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def insert_issue_type_html(icon, css, text):
    return mark_safe(f'<i class="bi bi-{icon} issue-type-{css}"></i> {text}')


def insert_issue_priority_html(icon, css, text):
    return mark_safe(f'<i class="bi bi-{icon} issue-priority-{css}"></i> {text}')


def insert_issue_status_html(css, text):
    return mark_safe(f'<span class="badge issue-status-{css}">{text.capitalize()}</span>')


@register.filter(is_safe=True)
def get_issue_type(issue_type):
    if issue_type == 'bug':
        return insert_issue_type_html('exclamation-square-fill', 'bug', 'Bug')
    elif issue_type == 'improvement':
        return insert_issue_type_html('arrow-up-square-fill', 'improvement', 'Improvement')
    elif issue_type == 'task':
        return insert_issue_type_html('check-square-fill', 'task', 'Task')
    return insert_issue_type_html('plus-square-fill', 'new-feature', 'New Feature')


@register.filter(is_safe=True)
def get_issue_priority(issue_priority):
    if issue_priority == 'highest':
        return insert_issue_priority_html('chevron-double-up', 'highest', 'Highest')
    elif issue_priority == 'high':
        return insert_issue_priority_html('chevron-up', 'high', 'High')
    elif issue_priority == 'medium':
        return insert_issue_priority_html('chevron-expand', 'medium', 'Medium')
    elif issue_priority == 'low':
        return insert_issue_priority_html('chevron-down', 'low', 'Low')
    return insert_issue_priority_html('chevron-double-down', 'lowest', 'Lowest')


@register.filter(is_safe=True)
def get_issue_status(issue_status):
    if issue_status in ('open', 'reopened'):
        return insert_issue_status_html('open', issue_status)
    elif issue_status == 'in_progress':
        return insert_issue_status_html('active', 'In progress')
    else:
        return insert_issue_status_html('closed', issue_status)


@register.filter()
def is_opened(issue_status):
    if issue_status in ('open', 'reopened'):
        return True
    return False