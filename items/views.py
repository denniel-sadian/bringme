from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'items/home.html'

    def get_context_data(self, **kwargs):
        kwargs['user'] = self.request.user
        return super().get_context_data(**kwargs)
