from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PacienteViewSet,
    UsuarioViewSet,
    PacienteUsuarioViewSet,
    DispositivoViewSet,
    AsignacionDispositivoViewSet,
    SesionSuenoViewSet,
    RegistroSaludViewSet,
    AlertaViewSet,
    ConfirmacionAlertaViewSet,
)

router = DefaultRouter()

router.register("pacientes", PacienteViewSet)
router.register("usuarios", UsuarioViewSet)
router.register("paciente-usuarios", PacienteUsuarioViewSet)
router.register("dispositivos", DispositivoViewSet)
router.register("asignaciones-dispositivos", AsignacionDispositivoViewSet)
router.register("sesiones-sueno", SesionSuenoViewSet)
router.register("registros-salud", RegistroSaludViewSet)
router.register("alertas", AlertaViewSet)
router.register("confirmaciones-alerta", ConfirmacionAlertaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]