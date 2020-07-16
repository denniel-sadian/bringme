from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_registration.forms import RegistrationForm

from .models import CustomUser


class CustomUserForm(RegistrationForm):
    
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ('email', 'name', 'address', 'contact_number', 'photo')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'address', 'contact_number', 'photo')
