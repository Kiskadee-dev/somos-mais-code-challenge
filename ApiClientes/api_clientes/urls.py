from api_clientes.views import Clientes
from django.urls import path

urlpatterns = [path("users/", Clientes.as_view())]
