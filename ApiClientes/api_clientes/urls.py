from api_clientes.views import Tags, Users, UsersByRegion, MainView, Regions
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
    path("", MainView.as_view(), name="main"),
    path("users", Users.as_view(), name="users"),
    path("users/region/", Regions.as_view(), name="regions"),
    path("users/region/tag/", Tags.as_view(), name="tags"),
    path("users/<str:region>", UsersByRegion.as_view(), name="users_by_region"),
    path(
        "users/<str:region>/<str:tag>",
        UsersByRegion.as_view(),
        name="users_by_region_and_tag",
    ),
]
