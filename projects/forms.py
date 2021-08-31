from django import forms
from django.apps import apps

from .models import Project, Member


class ProjectCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ('name', 'color')

    def save(self, commit=True):
        project = super(ProjectCreateForm, self).save(commit=False)
        if commit:
            project.save()
            Member.objects.create(
                user=self.user,
                project=project,
                role=3,
            )
            project.owner = apps.get_model('users.CustomUser').objects.get(id=self.user.id)
            project.save()
        return project