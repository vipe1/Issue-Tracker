import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from .forms import CustomUserCreationForm, AccountEditForm


# Create your views here.
class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'recaptcha_site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY
    }

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'response': recaptcha_response,
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY
            }
            req = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = req.json()

            if result['success']:
                return self.form_valid(form)
            form.add_error(None, 'Invalid reCAPTCHA. Please try again.')
        return self.form_invalid(form)


class AccountSettingsView(LoginRequiredMixin, UpdateView):
    form_class = AccountEditForm
    template_name = 'accounts/account_settings.html'
    success_url = reverse_lazy('account_settings')

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        account = self.request.user
        initial = {
            'email': account.email,
            'username': account.username,
        }
        return initial

    def get_form_kwargs(self):
        kwargs = super(AccountSettingsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AccountDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account_delete.html'

    def post(self, request):
        account = request.user
        account.delete()
        return HttpResponseRedirect(reverse_lazy('login'))
