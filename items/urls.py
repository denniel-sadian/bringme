from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('about/', views.AboutView.as_view(), name='about'),
    
    path('items/', views.ItemsListView.as_view(), name='items-list'),
    
    path('items/<int:pk>/close/',
         views.ItemCloseToggleRedirectView.as_view(),
         name='item-close-toggle'),
    
    path('items/<int:pk>/delivered/',
         views.ItemMarkDeliveredView.as_view(), name='item-delivered'),
    
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    
    path('items/update/<int:pk>/',
         views.ItemUpdateView.as_view(), name='item-update'),
    
    path('items/delete/<int:pk>/',
         views.ItemDeleteView.as_view(), name='item-delete'),
    
    path('items/create/', views.ItemCreateView.as_view(), name='item-create')
]
