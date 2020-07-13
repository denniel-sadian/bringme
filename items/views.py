from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Item


class HomeView(TemplateView):
    template_name = 'items/home.html'


class ItemsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
    context_object_name = 'items'

    def get_queryset(self):
        if 'address' in self.request.GET:
            get_address = self.request.GET['address']
            return Item.objects.filter(user__address__icontains=get_address,
                                       delivered=False)
        user_address = self.request.user.address
        return Item.objects.filter(user__address__icontains=user_address,
                                   delivered=False)


class ItemDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    model = Item
    fields = ('name', 'description', 'photo', 'expected_price', 'expected_store')
    template_name = 'items/item_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('accounts:login')
    model = Item
    fields = ('name', 'description', 'photo', 'expected_price', 'expected_store')
    template_name = 'items/item_update.html'

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
        user = self.request.user

        # Accept if it isn't the owner
        if item.user != user or not item.delivered:
            if not item.closed:
                item.closed = True
                item.closed_by = user
            # Open again if the user was the one who closed it
            elif item.closed_by == user:
                item.closed = False
                item.closed_by = None
            item.save()
        
        return super().get_redirect_url(*args, **kwargs)


class ItemMarkDeliveredView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Item
    context_object_name = 'item'

    def dispatch(self, *args, **kwargs):
        """
        Don't let users mark the items delivered if they are not closed
        yet or they're not the owner.
        """
        item = self.get_object()
        if not item.closed or item.user != self.request.user:
            return redirect(reverse_lazy('items:items-list'))
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request, 'items/item_confirm_delivered.html', {'item': self.get_object()})
    
    def post(self, request, *args, **kwargs):
        item = self.get_object()
        item.delivered = True
        item.closed_by.deliveries = item.closed_by.deliveries + 1
        item.closed_by.save()
        item.save()
        return redirect(reverse_lazy('items:item-detail', kwargs={'pk': item.id}))
