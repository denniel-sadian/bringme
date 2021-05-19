from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        'password_reset/',
        views.PasswordResetView.as_view(), name='password_reset'),
    path(
        '', include("django.contrib.auth.urls")
    ),
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name='django_registration_register'),
    path(
        'activate/<str:activation_key>/',
        views.AccountActivationView.as_view(),
        name='django_registration_activate',
    ),
    path(
        '',
        include('django_registration.backends.activation.urls')
    ),
    path(
        'profile-update/',
        views.UpdateUserView.as_view(),
        name='profile-update'),
]
