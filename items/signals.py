from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Item
from accounts.models import CustomUser
from accounts.emails import NewPostNotif
from accounts.emails import ClosedPostNotif
from accounts.emails import ItemDeliveredNotif
from accounts.emails import ItemCancelledNotif


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
    
    NewPostNotif(instance).send()


@receiver(pre_save, sender=Item)
def notify_user_on_post(sender, instance, **kwargs):
    if not instance.pk:
        return
    
    item = Item.objects.get(pk=instance.pk)

    # Closed
    if not item.closed and instance.closed:
        ClosedPostNotif(instance).send()
    
    # Canceled
    elif item.closed and not instance.closed:
        ItemCancelledNotif(instance).send()
    
    # Delivered
    if not item.delivered and instance.delivered:
        ItemDeliveredNotif(instance).send()