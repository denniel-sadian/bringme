from django.views.generic.edit import CreateView
from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView as PassResetView
from django.contrib.auth import login
from django.urls import reverse_lazy

from django_registration.backends.activation.views import RegistrationView
from django_registration.backends.activation.views import ActivationView

from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm
from .forms import CustomUserForm
from .models import CustomUser
from .emails import ActivationEmail


class UserRegisterView(RegistrationView):
    form_class = CustomUserForm


class UpdateUserView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile-update')
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_update.html'

    def get_object(self):
        return self.request.user
