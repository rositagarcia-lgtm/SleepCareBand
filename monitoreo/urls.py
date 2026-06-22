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
    ultimas_alertas
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

    # 🔐 LOGIN -> Accesible en: /api/login/
    path("login/", login_usuario),

    # 📡 DISPOSITIVOS -> Accesible en: /api/asignar-dispositivo/
    path("asignar-dispositivo/", asignar_dispositivo),

    # ❤️ SENSOR ESP32 -> Accesible en: /api/recibir-sensor/
    path("recibir-sensor/", recibir_datos_sensor),

    # 🚨 ALERTAS PARA ANDROID -> Accesible en: /api/ultimas_alertas/
    path("ultimas_alertas/", ultimas_alertas),
]