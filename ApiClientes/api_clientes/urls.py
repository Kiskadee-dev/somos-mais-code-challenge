from api_clientes.views import Clientes
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(), name="redoc"),
    path("users/", Clientes.as_view()),
]
