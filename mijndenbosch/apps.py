from django.apps import AppConfig

class Config(AppConfig):
    name = 'mijndenbosch'
    verbose_name = 'Mijn Den Bosch'

    def ready(self):
        from . import signals
