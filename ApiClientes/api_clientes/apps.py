from django.apps import AppConfig


class ApiClientesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api_clientes"

    def ready(self) -> None:
        print("ApiClient app Ready!")
        return super().ready()
