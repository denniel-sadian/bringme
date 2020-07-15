from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UpdateUserView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile-update')
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile_update.html'

    def get_object(self):
        return self.request.user
