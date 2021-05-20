from django.conf import settings
from django.contrib.sites.models import Site

from mailviews.messages import TemplatedHTMLEmailMessageView

from accounts.models import CustomUser


class BaseTemplatedHTMLEmailMessageView(TemplatedHTMLEmailMessageView):
    """Base templated HTML email message view class."""

    def get_context_data(self, **kwargs):
        """Return context data for the templates."""
        if 'protocol' not in kwargs:
            kwargs['protocol'] = (
                'http{}'.format('s' if settings.USE_HTTPS else ''))
        
        site = Site.objects.get_current()
        if 'domain' not in kwargs:
            kwargs['domain'] = site.domain
        
        # workaround to fully qualify static URLs in development or
        # for misconfigured STATIC_URL
        if 'http' not in settings.STATIC_URL:
            # development or misconfigured STATIC_URL
            kwargs.update({
                'STATIC_PREFIX': 'http{}://{}'.format(
                    's' if settings.USE_HTTPS else '',
                    site.domain)
            })
        else:
            # production; no need for workaround
            context['STATIC_PREFIX'] = ''

        return super().get_context_data(**kwargs)


class PostInstanceMixin:
    
    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post = post

    def get_context_data(self, **kwargs):
        context = {
            'post': self.post
        }
        context.update(kwargs)

        return super().get_context_data(**context)


class NewPostNotif(PostInstanceMixin, BaseTemplatedHTMLEmailMessageView):
    subject_template_name = 'accounts/emails/new/subject.txt'
    body_template_name = 'accounts/emails/new/body.txt'
    html_body_template_name = (
        'accounts/emails/new/body.html')

    def render_to_message(self, *args, **kwargs):
        address = self.post.user.address
        to_emails = set()
        for rider in CustomUser.objects.filter(is_rider=True):
            rider_addr = rider.address.split(',')[-1]
            if rider_addr in address and rider != self.post.user:
                to_emails.add(rider.email)
        
        kwargs['to'] = to_emails
        return super().render_to_message(*args, **kwargs)


class ClosedPostNotif(PostInstanceMixin, BaseTemplatedHTMLEmailMessageView):
    subject_template_name = 'accounts/emails/closed/subject.txt'
    body_template_name = 'accounts/emails/closed/body.txt'
    html_body_template_name = (
        'accounts/emails/closed/body.html')
    
    def render_to_message(self, *args, **kwargs):
        kwargs['to'] = (self.post.user.email,)
        return super().render_to_message(*args, **kwargs)


class ItemCancelledNotif(PostInstanceMixin, BaseTemplatedHTMLEmailMessageView):
    subject_template_name = 'accounts/emails/cancelled/subject.txt'
    body_template_name = 'accounts/emails/cancelled/body.txt'
    html_body_template_name = (
        'accounts/emails/cancelled/body.html')
    
    def render_to_message(self, *args, **kwargs):
        kwargs['to'] = (self.post.user.email,)
        return super().render_to_message(*args, **kwargs)


class ItemDeliveredNotif(PostInstanceMixin, BaseTemplatedHTMLEmailMessageView):
    subject_template_name = 'accounts/emails/delivered/subject.txt'
    body_template_name = 'accounts/emails/delivered/body.txt'
    html_body_template_name = (
        'accounts/emails/delivered/body.html')
    
    def render_to_message(self, *args, **kwargs):
        kwargs['to'] = (self.post.closed_by.email,)
        return super().render_to_message(*args, **kwargs)


class ActivationEmail(BaseTemplatedHTMLEmailMessageView):
    subject_template_name = 'accounts/emails/activation/subject.txt'
    body_template_name = 'accounts/emails/activation/body.txt'
    html_body_template_name = (
        'accounts/emails/activation/body.html')
    
    def __init__(self, user, context, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.context = context

    def get_context_data(self, **kwargs):
        context = {
            'user': self.user,
            'site': self.context['site'],
            'scheme': self.context['scheme'],
            'activation_key': self.context['activation_key']
        }
        context.update(kwargs)

        return super().get_context_data(**context)
    
    def render_to_message(self, *args, **kwargs):
        kwargs['to'] = (self.user.email,)
        return super().render_to_message(*args, **kwargs)