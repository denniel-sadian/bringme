from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import Item


class HomeView(TemplateView):
    template_name = 'items/home.html'


class ItemsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')

    def get_queryset(self):
        return Item.objects.filter(delivered=False)


class ItemDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    model = Item
    fields = ('name', 'description', 'photo', 'expected_price', 'expected_store')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
