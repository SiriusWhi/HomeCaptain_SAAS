from django.apps import AppConfig, apps


class PropertyConfig(AppConfig):
    name = 'apps.property'
    
    def ready(self):
        import apps.property.signals.handlers
        from actstream import registry
        registry.register(self.get_model('Property'))
