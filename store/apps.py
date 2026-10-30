import sys
from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # Automatically run migrations on startup (Free Tier Fix)
        if 'runserver' not in sys.argv and 'gunicorn' in sys.argv[0]:
            try:
                from django.core.management import call_command
                call_command('migrate', interactive=False)
            except Exception as e:
                print(f"Migration on startup error: {e}")