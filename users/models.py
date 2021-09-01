from django.contrib.auth.models import AbstractUser

from projects.models import Project


class CustomUser(AbstractUser):
    def __str__(self):
        return self.get_full_name()

    @property
    def projects(self):
        ids = self.memberships.values_list('project', flat=True)
        return Project.objects.filter(id__in=ids)
