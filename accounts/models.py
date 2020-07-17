from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail

from django_resized import ResizedImageField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=12)
    photo = ResizedImageField(size=[400, 400], upload_to='profiles', force_format='PNG')
    deliveries = models.IntegerField(default=0)
    is_rider = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.address = self.address.upper().replace(' ', '')
        super().save(*args, **kwargs)
    
    def email_user(self, *args, **kwargs):
        send_mail(
            '{}'.format(args[0]),
            '{}'.format(args[1]),
            '{}'.format(args[2]),
            [self.email],
            fail_silently=False
        )
