from django.db import models

from django_resized import ResizedImageField

from accounts.models import CustomUser


class Item(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    expected_price = models.IntegerField(default=0)
    expected_store = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    closed_bi = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
