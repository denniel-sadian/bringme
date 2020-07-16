from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', views.UserRegisterView.as_view(), name='django_registration_register'),
    path('', include('django_registration.backends.activation.urls')),
    path('profile-update/', views.UpdateUserView.as_view(), name='profile-update')
]
