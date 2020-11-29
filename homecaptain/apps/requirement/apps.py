from django.apps import AppConfig, apps

class RequirementConfig(AppConfig):
    name = 'apps.requirement'

    def ready(self):
        import apps.requirement.signals.handlers
        from actstream import registry
        registry.register(self.get_model('Requirement'))
