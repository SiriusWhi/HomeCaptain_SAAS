from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'apps.hcauth'

    def ready(self):
        import apps.hcauth.signals.handlers
