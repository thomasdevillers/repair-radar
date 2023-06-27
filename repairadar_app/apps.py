from django.apps import AppConfig


class RepairadarAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repairadar_app'

    def ready(self):
        import repairadar_app.signals
