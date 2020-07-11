from django.urls import path

from . import views

app_name = 'items'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('items/', views.ItemsListView.as_view(), name='items-list'),
    path('items/detail/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/update/<int:pk>/', views.ItemUpdateView.as_view(), name='item-update'),
    path('items/create/', views.ItemCreateView.as_view(), name='item-create')
]
