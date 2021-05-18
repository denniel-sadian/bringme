from django.db import models
from django.urls import reverse

from django_resized import ResizedImageField

from accounts.models import CustomUser


class Item(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = ResizedImageField(size=[600, 600], upload_to='items', force_format='PNG')
    expected_price = models.PositiveIntegerField(default=0)
    expected_store = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    closed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
