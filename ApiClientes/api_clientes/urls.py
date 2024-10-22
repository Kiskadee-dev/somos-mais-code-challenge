from api_clientes.views import Users, UsersByRegion
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
    path("users", Users.as_view(), name="users"),
    path("users/<str:region>", UsersByRegion.as_view(), name="users_by_region"),
    path(
        "users/<str:region>/<str:tag>",
        UsersByRegion.as_view(),
        name="users_by_region_and_tag",
    ),
]
