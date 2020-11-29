from django.apps import AppConfig


class CustomerConfig(AppConfig):
    ##https://stackoverflow.com/questions/44363793/how-to-set-default-app-config-for-django-with-apps-directory-structure
    name = 'apps.customer'

    def ready(self):
        #https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
        import apps.customer.signals.handlers
        from actstream import registry
        registry.register(self.get_model('Customer'))
