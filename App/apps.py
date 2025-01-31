from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'

    def ready(self):
        import App.signals  # Asegúrate de importar el archivo donde están las señales

class HallazgosConfig(AppConfig):
    name = 'hallazgos'

    def ready(self):
        import hallazgos.signals