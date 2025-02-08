    
# apps.py
from django.apps import AppConfig

class TeleconsultAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teleconsult_app'
    
    def ready(self):
        import teleconsult_app.signals

