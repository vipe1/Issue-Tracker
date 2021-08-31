from django import forms

from .models import Issue, Comment


class IssueCreateEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('name', 'description', 'type', 'priority')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)