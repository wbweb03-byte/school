from django.apps import AppConfig


class IdCardConfig(AppConfig):
    name = 'id_card'

def ready(self):
    import id_card.signals