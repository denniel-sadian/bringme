from django.contrib import admin

from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'closed', 'closed_by', 'delivered', 'date')


admin.site.register(Item, ItemAdmin)
