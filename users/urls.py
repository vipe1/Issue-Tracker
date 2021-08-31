from django.urls import path
from .views import SignupView, AccountSettingsView, AccountDeleteView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('account-settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('account-delete/', AccountDeleteView.as_view(), name='account_delete')
]
