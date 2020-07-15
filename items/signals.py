from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Item
from accounts.models import CustomUser


def notify_users(subject, to, html_message):
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    if len(to):
        send_mail(subject, plain_message, from_email, [to],
                  html_message=html_message, fail_silently=False)


@receiver(post_save, sender=Item)
def notify_users_on_new_post(sender, instance, created, **kwargs):
    if not created:
        return
    
    address = instance.user.address
    
    to_emails = []
    for user in CustomUser.objects.all():
        if user.address in address and user != instance.user:
            to_emails.append(user.email)
    
    html_message = render_to_string('items/notif_new_post.html', {'post': instance})
    notify_users('New Post Near You', to_emails, html_message)


@receiver(pre_save, sender=Item)
def notify_user_on_post(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    item = Item.objects.get(pk=instance.pk)
    
    # Undo
    if item.closed and not instance.closed:
        html_message = render_to_string('items/notif_undo.html', {'post': item})
        notify_users('Post Canceled', [item.user.email], html_message)
    
    # Close
    elif not item.closed and instance.closed:
        html_message = render_to_string('items/notif_closed_post.html', {'post': instance})
        notify_users('Post Closed', [item.user.email], html_message)
