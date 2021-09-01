from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from simple_history.models import HistoricalRecords

from custom.methods import get_random_slug
from projects.models import Project
from .constants import *


class IssueManager(models.Manager):
    def open(self):
        return self.filter(
            Q(status='open') | Q(status='reopened')
        )

    def active(self):
        return self.filter(
            status='in_progress'
        )

    def closed(self):
        return self.filter(
            Q(status='resolved') | Q(status='closed')
        )


# Create your models here.
class Issue(models.Model):
    objects = IssueManager()
    history = HistoricalRecords()

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=6, blank=True, unique=True)

    type = models.CharField(max_length=12, choices=ISSUE_TYPES, default='bug')
    priority = models.CharField(max_length=12, choices=ISSUE_PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=12, choices=ISSUE_STATUSES, default='open')

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='created_issues'
    )
    assignee = models.ForeignKey(
        'users.CustomUser',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_issues',
    )

    def __str__(self):
        return f'{self.project} - {self.name}'

    def save(self, *args, **kwargs):
        get_random_slug(self)
        super(Issue, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('issue_details', args=[self.project.slug, self.slug])


class Comment(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255, verbose_name='Comment')
