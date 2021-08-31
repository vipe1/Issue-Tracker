ISSUE_TYPES = (
    ('bug', 'Bug'),
    ('improvement', 'Improvement'),
    ('task', 'Task'),
    ('new_feature', 'New feature'),
)

ISSUE_PRIORITY_LEVELS = (
    ('highest', 'Highest'),
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
    ('lowest', 'Lowest'),
)

ISSUE_STATUSES = (
    ('Open', (
        ('open', 'Open'),
        ('reopened', 'Reopened'),
    )),
    ('Active', (
        ('in_progress', 'In progress'),
    )),
    ('Closed', (
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )),
)
