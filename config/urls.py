from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from inventory.views import (
    EquipmentViewSet,
    UsuarioViewSet,
    TerrenoViewSet,
    ViviendaViewSet,
    PuntoAccesoViewSet,
    ResidenteViewSet
)

router = DefaultRouter()

router.register("equipos", EquipmentViewSet, basename="equipment")
router.register("usuarios", UsuarioViewSet)
router.register("terrenos", TerrenoViewSet)
router.register("viviendas", ViviendaViewSet)
router.register("puntos-acceso", PuntoAccesoViewSet)
router.register("residentes", ResidenteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
