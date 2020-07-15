from django.apps import AppConfig


class ItemsConfig(AppConfig):
    name = 'items'

    def ready(self):
        from . import signals