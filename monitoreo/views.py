from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import (
    Paciente,
    Usuario,
    PacienteUsuario,
    Dispositivo,
    AsignacionDispositivo,
    SesionSueno,
    RegistroSalud,
    Alerta,
    ConfirmacionAlerta,
)

from .serializers import (
    PacienteSerializer,
    UsuarioSerializer,
    PacienteUsuarioSerializer,
    DispositivoSerializer,
    AsignacionDispositivoSerializer,
    SesionSuenoSerializer,
    RegistroSaludSerializer,
    AlertaSerializer,
    ConfirmacionAlertaSerializer,
)

# =========================
# VIEWSETS CRUD
# =========================

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PacienteUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PacienteUsuario.objects.all()
    serializer_class = PacienteUsuarioSerializer

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

class AsignacionDispositivoViewSet(viewsets.ModelViewSet):
    queryset = AsignacionDispositivo.objects.all()
    serializer_class = AsignacionDispositivoSerializer

class SesionSuenoViewSet(viewsets.ModelViewSet):
    queryset = SesionSueno.objects.all()
    serializer_class = SesionSuenoSerializer

class RegistroSaludViewSet(viewsets.ModelViewSet):
    queryset = RegistroSalud.objects.all()
    serializer_class = RegistroSaludSerializer

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer

class ConfirmacionAlertaViewSet(viewsets.ModelViewSet):
    queryset = ConfirmacionAlerta.objects.all()
    serializer_class = ConfirmacionAlertaSerializer


# =========================
# LOGIN
# =========================

@api_view(["POST"])
def login_usuario(request):
    correo = request.data.get("correo")
    password = request.data.get("password")

    try:
        usuario = Usuario.objects.get(correo=correo, password=password)

        return Response({
            "success": True,
            "id": usuario.id,
            "nombres": usuario.nombres,
            "correo": usuario.correo,
            "rol": usuario.rol
        })

    except Usuario.DoesNotExist:
        return Response({
            "success": False,
            "message": "Correo o contraseña incorrectos"
        })


# =========================
# ASIGNAR DISPOSITIVO
# =========================

@api_view(["POST"])
def asignar_dispositivo(request):

    codigo = request.data.get("codigo_pulsera")
    paciente_id = request.data.get("paciente_id")
    fecha_inicio = request.data.get("fecha_inicio")
    fecha_fin = request.data.get("fecha_fin")

    try:
        dispositivo = Dispositivo.objects.get(codigo_pulsera=codigo)
        paciente = Paciente.objects.get(id=paciente_id)

        AsignacionDispositivo.objects.create(
            paciente=paciente,
            dispositivo=dispositivo,
            fecha_inicio=fecha_inicio or timezone.now().date(),
            fecha_fin=fecha_fin
        )

        return Response({
            "success": True,
            "message": "Dispositivo asignado correctamente"
        })

    except Exception as e:
        return Response({
            "success": False,
            "message": str(e)
        })


# =========================
# 🚨 SENSOR + MOVIMIENTO + ALERTAS
# =========================

@api_view(["POST"])
def recibir_datos_sensor(request):

    codigo = request.data.get("codigo_pulsera")
    ritmo = request.data.get("ritmo_cardiaco")
    spo2 = request.data.get("spo2")
    temperatura = request.data.get("temperatura")
    movimiento = request.data.get("movimiento", "normal")

    try:
        dispositivo = Dispositivo.objects.filter(codigo_pulsera=codigo).first()

        if not dispositivo:
            return Response({
                "success": False,
                "estado": "sin_senal",
                "message": "Dispositivo no encontrado"
            })

        asignacion = AsignacionDispositivo.objects.filter(dispositivo=dispositivo).first()

        if not asignacion:
            return Response({
                "success": False,
                "estado": "sin_senal",
                "message": "Dispositivo no asignado"
            })

        paciente = asignacion.paciente

        sesion = SesionSueno.objects.filter(paciente=paciente).last()

        if not sesion:
            sesion = SesionSueno.objects.create(
                paciente=paciente,
                fecha=timezone.now().date(),
                hora_inicio=timezone.now(),
                hora_fin=timezone.now()
            )

        # =========================
        # CONVERSIÓN SEGURA
        # =========================
        ritmo = int(ritmo) if ritmo not in [None, ""] else 0
        spo2 = int(spo2) if spo2 not in [None, ""] else 0
        temperatura = float(temperatura) if temperatura not in [None, ""] else 0

        # =========================
        # LÓGICA
        # =========================
        alerta_texto = None
        tipo_alerta = None
        estado = "normal"
        recomendacion = "Paciente estable"

        # 🔴 CRÍTICO
        if spo2 < 88 or ritmo > 130 or temperatura > 38.5 or movimiento == "critico":
            estado = "critico"
            alerta_texto = "Estado crítico detectado"
            tipo_alerta = "critica"
            recomendacion = "🚨 Emergencia médica inmediata"

        # 🟠 INESTABLE
        elif spo2 < 92 or ritmo > 120 or temperatura > 38 or movimiento == "agitado":
            estado = "inestable"
            alerta_texto = "Valores inestables"
            tipo_alerta = "alta"
            recomendacion = "⚠️ Monitoreo constante"

        # 🟡 LEVE
        elif ritmo > 100 or movimiento == "leve":
            estado = "alerta"
            alerta_texto = "Frecuencia o movimiento elevado"
            tipo_alerta = "media"
            recomendacion = "Descanso recomendado"

        # =========================
        # REGISTRO
        # =========================
        RegistroSalud.objects.create(
            sesion=sesion,
            fecha_hora=timezone.now(),
            ritmo_cardiaco=ritmo,
            spo2=spo2,
            temperatura=temperatura,
            movimiento=movimiento,
            alerta=alerta_texto is not None,
            tipo_alerta=tipo_alerta
        )

        # =========================
        # EVITAR SPAM ALERTAS (30s)
        # =========================
        ultima = Alerta.objects.filter(paciente=paciente).order_by("-fecha_hora").first()

        crear_alerta = True
        if ultima:
            if timezone.now() - ultima.fecha_hora < timedelta(seconds=30):
                crear_alerta = False

        if alerta_texto and crear_alerta:
            Alerta.objects.create(
                paciente=paciente,
                fecha_hora=timezone.now(),
                tipo_alerta=tipo_alerta,
                descripcion=alerta_texto,
                estado=estado
            )

        return Response({
            "success": True,
            "estado": estado,
            "alerta": alerta_texto,
            "recomendacion": recomendacion
        })

    except Exception as e:
        return Response({
            "success": False,
            "message": str(e)
        })


# =========================
# ALERTAS ANDROID
# =========================

@api_view(["GET"])
def ultimas_alertas(request):

    paciente_id = request.query_params.get("paciente_id")

    if not paciente_id:
        return Response({
            "success": False,
            "message": "Falta paciente_id"
        })

    alertas = Alerta.objects.filter(
        paciente_id=paciente_id
    ).order_by("-fecha_hora")[:10]

    return Response({
        "success": True,
        "alertas": [
            {
                "id": a.id,
                "tipo_alerta": a.tipo_alerta,
                "descripcion": a.descripcion,
                "estado": a.estado,
                "fecha_hora": a.fecha_hora
            }
            for a in alertas
        ]
    })