from django.apps import AppConfig

from api_clientes.clients.datarepo import DataRepo


class ApiClientesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api_clientes"

    def ready(self) -> None:
        print("ApiClient app Ready!")
        DataRepo().get_data()
        return super().ready()
