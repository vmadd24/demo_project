from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Seed admin user and sample products once per process boot.
        from .seed import seed_all

        seed_all()
