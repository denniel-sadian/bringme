from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from .models import Item


class HomeView(TemplateView):
    template_name = 'items/home.html'


class ItemsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        return Item.objects.filter(delivered=False)
