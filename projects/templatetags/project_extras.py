from django import template

register = template.Library()

@register.filter()
def is_opened(issue_status):
    if issue_status in ('open', 'reopened'):
        return True
    return False