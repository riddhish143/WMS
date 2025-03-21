from django.apps import AppConfig


class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        from weather import updater
        updater.start()