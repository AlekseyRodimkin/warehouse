from django.apps import AppConfig


class BoundConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bound"

    def ready(self):
        from . import signals
