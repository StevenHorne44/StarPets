from django.apps import AppConfig


class PetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pets'
    
    def ready(self):
        # Connect signal handlers when the app initializes
        import pets.signals
