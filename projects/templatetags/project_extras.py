from django import template
from django.core.exceptions import FieldError

register = template.Library()

@register.filter()
def is_opened(issue_status):
    if issue_status in ('open', 'reopened'):
        return True
    return False

@register.filter()
def issues_assigned_to_user(issues, user):
    return issues.filter(assignee=user)

@register.filter()
def issues_sort(issues_qs, sort_by):
    try:
        return issues_qs.order_by(sort_by, 'name')
    except FieldError:
        return issues_qs