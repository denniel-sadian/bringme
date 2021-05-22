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


class AboutView(TemplateView):
    template_name = 'items/about.html'


class ItemsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = Item.objects.filter(delivered=False, closed=False)
        
        # The user is a rider.
        if self.request.user.is_rider:
            # Get posts based from the given filter.
            if 'address' in self.request.GET and self.request.GET['address']:
                get_address = self.request.GET['address']
                get_address = get_address.upper().replace(' ', '')
                queryset = queryset.filter(user__address__icontains=get_address)
            # Get post based from the rider's address.
            else:
                user_address = self.request.user.address.split(',')[-1]
                queryset = queryset.filter(user__address__icontains=user_address)
        
        # The user is just a regular user, so just get his or her posts.
        else:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset.order_by('-pk')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_items_closed'] = self.request.user.items.filter(
            closed=True, delivered=False)
        context['items_closed_by_user'] = Item.objects.filter(
            closed_by=self.request.user, delivered=False).order_by('-date')
        context['items_delivered_by_user'] = Item.objects.filter(
            closed_by=self.request.user, delivered=True).order_by('-date')[:10]
        return context


class ItemDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Item
    fields = ('name', 'description', 'photo', 'expected_price', 'expected_store')
    template_name = 'items/item_create.html'

    def dispatch(self, *args, **kwargs):
        # Don't let riders create posts.
        if self.request.user.is_rider:
            return redirect(reverse_lazy('items-list'))

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Item
    fields = ('name', 'description', 'photo', 'expected_price', 'expected_store')
    template_name = 'items/item_update.html'

    def dispatch(self, *args, **kwargs):
        post = self.get_object()
        
        # Don't update closed posts.
        if post.closed:
            return redirect(reverse_lazy('items-list'))
        
        # Only owners will update their posts.
        if self.request.user != post.user:
            return redirect(reverse_lazy('items-list'))

        return super().dispatch(*args, **kwargs)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('items-list')
    model = Item

    def dispatch(self, *args, **kwargs):
        post = self.get_object()
        
        # Don't let users delete items if they've been closed already
        # or they're not the owner of the post.
        if post.closed or post.user != self.request.user:
            return redirect(reverse_lazy('items-list'))
        return super().dispatch(*args, **kwargs)


class ItemCloseToggleRedirectView(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy('login')
    permanent = False
    query_string = True
    pattern_name = 'item-detail'

    def get_redirect_url(self, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        user = self.request.user

        # Accept if it isn't the owner
        if item.user != user and not item.delivered and user.is_rider:
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
            return redirect(reverse_lazy('items-list'))
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request, 'items/item_confirm_delivered.html', {'item': self.get_object()})
    
    def post(self, request, *args, **kwargs):
        item = self.get_object()
        item.delivered = True
        item.closed_by.deliveries += 1
        item.closed_by.save()
        item.save()
        return redirect(reverse_lazy('items-list'))
