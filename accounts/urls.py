from django.conf.urls import include
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile-update/', views.UpdateUserView.as_view(), name='profile-update')
]