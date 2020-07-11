from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Item


class HomeView(TemplateView):
    template_name = 'items/home.html'


class ItemsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
    context_object_name = 'items'

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


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('accounts:login')
    model = Item
    fields = ('name', 'description', 'photo', 'expected_price', 'expected_store')

    def dispatch(self, *args, **kwargs):
        """
        Don't let users update items if they've been closed already.
        """
        if self.get_object().closed:
            return redirect(reverse_lazy('items:items-list'))
        return super().dispatch(*args, **kwargs)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('items:items-list')
    model = Item

    def dispatch(self, *args, **kwargs):
        """
        Don't let users delete items if they've been closed already
        or they're not the owner of the item.
        """
        item = self.get_object()
        if item.closed or item.user != self.request.user:
            return redirect(reverse_lazy('items:items-list'))
        return super().dispatch(*args, **kwargs)


class ItemCloseToggleRedirectView(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy('accounts:login')
    permanent = False
    query_string = True
    pattern_name = 'items:item-detail'

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        if item.user != self.request.user:
            if not item.closed:
                item.closed = True
                item.closed_by = self.request.user
            else:
                item.closed = False
                item.closed_by = None
            item.save()
        return super().get_redirect_url(*args, **kwargs)
