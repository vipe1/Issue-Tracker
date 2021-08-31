from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Given email is already in use')
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Given email is already in use')
        return email


class AccountEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        kwargs.pop('instance')  # It prevents unexpected 'instance' error
        super().__init__(*args, **kwargs)

    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('''Username can't contain spaces''')
        account = CustomUser.objects.exclude(pk=self.user.pk).filter(username=username).first()
        if account is None:
            return username
        raise forms.ValidationError('Given username is already in use')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError('Given email is already in use')
        return email

    def save(self):
        account = self.user
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.save()
        return account
