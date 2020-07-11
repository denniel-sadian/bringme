from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .forms import CustomUserChangeForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')


class UpdateUserView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('accounts:profile-update')

    def get_object(self):
        return self.request.user
