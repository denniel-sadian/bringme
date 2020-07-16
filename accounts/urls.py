from django.conf.urls import include
from django.urls import path

from django_registration.backends.activation.views import RegistrationView

from . import views
from .forms import CustomUserForm

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/',
        RegistrationView.as_view(
            form_class=CustomUserForm
        ),
        name='django_registration_register',
    ),
    path('', include('django_registration.backends.activation.urls')),
    path('profile-update/', views.UpdateUserView.as_view(), name='profile-update')
]
