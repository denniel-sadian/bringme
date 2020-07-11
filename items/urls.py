from django.urls import path

from . import views

app_name = 'items'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('items/', views.ItemsListView.as_view(), name='items-list'),
    path('items/create/', views.ItemCreateView.as_view(), name='item-create')
]
