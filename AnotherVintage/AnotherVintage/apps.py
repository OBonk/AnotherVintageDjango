from django.apps import AppConfig
from django.apps import apps as django_apps

class AnotherVintageConfig(AppConfig):
    name = 'AnotherVintage'

    def ready(self):
        # import signal handlers
        import AnotherVintage.signal