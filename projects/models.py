from django.db import models
from django.apps import apps
from django.shortcuts import reverse
from colorfield.fields import ColorField

from custom.methods import get_random_slug


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=40, blank=True)
    color = ColorField(format='hex', default='#ffffff')
    owner = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_projects'
    )

    @property
    def users(self):
        return apps.get_model('users.CustomUser').objects.filter(id__in=self.members.values_list('user', flat=True))

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        get_project_slug(self)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', args=[self.slug])


class Member(models.Model):
    class MemberRoles(models.IntegerChoices):
        ADMIN = 3, 'Admin'
        DEVELOPER = 2, 'Developer'
        SPECTATOR = 1, 'Spectator'

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.PositiveSmallIntegerField(
        choices=MemberRoles.choices,
        default=MemberRoles.SPECTATOR
    )

    def __str__(self):
        return f'{self.project} - {self.user}'

    def get_absolute_url(self):
        return reverse('member_detail', args=[self.project.slug, self.id])

    @property
    def is_owner(self):
        return self.user == self.project.owner


class ProjectInvitation(models.Model):
    class InviteStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='invites'
    )
    status = models.CharField(
        max_length=12,
        choices=InviteStatus.choices,
        default=InviteStatus.ACTIVE
    )
    slug = models.SlugField(max_length=6, blank=True)

    def __str__(self):
        return f'{self.project} invitation ({self.id})'

    def save(self, *args, **kwargs):
        get_random_slug(self)
        super(ProjectInvitation, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_invite', args=[self.slug])


# Get unique slug function
def get_project_slug(project: Project):
    if not project.slug:
        # Slugify project's name
        slug = project.name[:31].strip().lower().replace(' ', '-')
        slug = ''.join(e for e in slug if e.isalnum() or e == '-' or e == '_')

        # Get list of slugs that could be similar
        other_simmiliar_project_slugs = list(Project.objects.filter(
            slug__startswith=slug
        ).values_list('slug', flat=True))
        if len(other_simmiliar_project_slugs) == 0:
            project.slug = slug
        else:
            i = 1
            while not project.slug:
                new_slug = f'{slug}{i}'
                if new_slug not in other_simmiliar_project_slugs:
                    project.slug = new_slug
                else:
                    i += 1
    '''

    There's a possibility that if 1 billion projects would take the same name (with 31+ chars),
    function would overextend slug's field max_length.
    However, because it's not a commercial project,
    I don't assume I'll ever have even thousand projects in here;
    hence, I'm not going to write a logic that would prevent this kind of situation.

    '''
