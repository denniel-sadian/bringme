from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Item
from accounts.models import CustomUser


@receiver(post_save, sender=Item)
def notify_users(sender, instance, **kwargs):
    address = instance.user.address
    
    to_emails = []
    for user in CustomUser.objects.all():
        if user.address in address:
            to_email.append(user.email)
    
    html_message = render_to_string('items/new_post_notif.html', {'post': instance})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL

    if len(to_emails):
        send_mail('New Post Near You', plain_message, from_email, [to_emails],
                  html_message=html_message, fail_silently=False)
