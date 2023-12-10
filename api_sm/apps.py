from django.apps import AppConfig


class ApiSmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_sm'

    def ready(self):
        import api_sm.Signals
