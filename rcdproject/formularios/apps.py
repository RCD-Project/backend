from django.apps import AppConfig


class FormulariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'formularios'

    def ready(self):
        import formularios.signals

