from django.apps import AppConfig


class CrimsonmatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crimsonmatch'

def ready(self):
    import crimsonmatch.signals
