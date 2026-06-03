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
    login_usuario,
    asignar_dispositivo,
    recibir_datos_sensor,
    ultimas_alertas   # 👈 IMPORTANTE
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

    # 🔐 LOGIN
    path("login/", login_usuario),

    # 📡 DISPOSITIVOS
    path("asignar-dispositivo/", asignar_dispositivo),

    # ❤️ SENSOR ESP32
    path("recibir-sensor/", recibir_datos_sensor),

    # 🚨 NUEVO: ALERTAS PARA ANDROID
    path("ultimas_alertas/", ultimas_alertas),
]