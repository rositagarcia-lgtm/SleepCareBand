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


# ========================================================
# 🚨 TELEMETRÍA MÉDICA AVANZADA (OMS / AHA / BATERÍA)
# ========================================================

@api_view(["POST"])
def recibir_datos_sensor(request):
    codigo = request.data.get("codigo_pulsera")
    ritmo = request.data.get("ritmo_cardiaco")
    spo2 = request.data.get("spo2")
    temperatura = request.data.get("temperatura")
    movimiento = request.data.get("movimiento", "normal") 
    boton_panico = request.data.get("boton_panico", False) 
    bateria = request.data.get("bateria", 100)  # Captura la telemetría de la batería

    try:
        # --- VERIFICACIONES DE HARDWARE Y ASIGNACIÓN ---
        dispositivo = Dispositivo.objects.filter(codigo_pulsera=codigo).first()

        if not dispositivo:
            return Response({
                "success": False,
                "estado": "sin_senal",
                "message": "Dispositivo no encontrado"
            })

        asignacion = AsignacionDispositivo.objects.filter(dispositivo=dispositivo).last()

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
                hora_inicio=timezone.now()
            )

        # --- CONVERSIÓN Y SANITIZACIÓN SEGURA ---
        ritmo = int(ritmo) if ritmo not in [None, ""] else 0
        spo2 = int(spo2) if spo2 not in [None, ""] else 0
        temperatura = float(temperatura) if temperatura not in [None, ""] else 0.0
        es_panico = boton_panico in [True, "true", "True", 1]

        # ========================================================
        # 🚨 SISTEMA DE TRIAJE MÉDICO BASADO EN CRITERIOS GERIÁTRICOS
        # ========================================================
        alerta_texto = None
        tipo_alerta = None
        estado = "normal"
        recomendacion = "Paciente estable. Constantes vitales dentro de los rangos normales de la OMS."

        # 1. CANAL PRIORITARIO A: BOTÓN DE PÁNICO (Emergencia Manual Inmediata)
        if es_panico:
            estado = "critico"
            alerta_texto = "¡EMERGENCIA MANUAL! El paciente pulsó el botón de auxilio."
            tipo_alerta = "critica"
            recomendacion = "🚨 Asistencia inmediata: El paciente reporta malestar grave o desorientación."

        # 2. CANAL PRIORITARIO B: PULSERA EN ESPERA (Fuera del cuerpo / Reposo)
        elif movimiento == "en espera":
            RegistroSalud.objects.create(
                sesion=sesion,
                fecha_hora=timezone.now(),
                ritmo_cardiaco=ritmo,
                spo2=spo2,
                temperatura=temperatura,
                movimiento=movimiento,
                alerta=False,
                tipo_alerta=None
            )
            return Response({
                "success": True,
                "estado": "en espera",
                "alerta": None,
                "recomendacion": "Dispositivo en reposo. Coloque la pulsera en el paciente.",
                "bateria_recibida": bateria
            })

        # 3. CANAL AUTOMÁTICO: EVALUACIÓN DE CRITERIOS CLÍNICOS (Adulto Mayor)
        else:
            # 🔴 UMBRAL CRÍTICO (Prioridad Absoluta a la Hipoxia Severa y Caídas)
            # - SpO2 < 90%: Criterio OMS de Insuficiencia Respiratoria Aguda.
            # - Ritmo > 130 lpm o < 40 lpm: Taquicardia extrema en reposo / Bloqueo cardíaco senil.
            # - Temperatura > 38.8 °C: Hipertermia crítica o choque séptico.
            # - Movimiento: Impacto crítico (Caída).
            if (0 < spo2 < 90) or (ritmo > 130) or (0 < ritmo < 40) or (temperatura > 38.8) or (movimiento in ["critico", "caida fuerte"]):
                estado = "critico"
                tipo_alerta = "critica"
                
                if 0 < spo2 < 90:
                    alerta_texto = f"Emergencia: Hipoxia severa detectada (SpO2: {spo2}%)."
                    recomendacion = "🚨 CRÍTICO: Saturación de oxígeno peligrosa. Despierte al paciente y proporcione soporte respiratorio inmediato."
                elif movimiento in ["critico", "caida fuerte"]:
                    alerta_texto = "Emergencia: Acelerómetro detectó impacto por caída fuerte."
                    recomendacion = "🚨 CRÍTICO: Posible caída. Acuda inmediatamente a verificar traumatismos."
                else:
                    alerta_texto = "Emergencia: Desbalance hemodinámico o térmico crítico."
                    recomendacion = "🚨 CRÍTICO: Ritmo cardíaco o temperatura en rangos de riesgo vital."

            # 🟠 UMBRAL INESTABLE / ALERTA ALTA (Monitoreo Clínico Obligatorio)
            # - SpO2 90% - 93%: Hipoxia clínica temprana (OMS).
            # - Ritmo 105 - 130 lpm o 40 - 49 lpm: Ritmo inestable en reposo (AHA).
            # - Temperatura > 37.8 °C: Síndrome febril geriátrico temprano.
            # - Movimiento: Agitación psicomotriz o convulsión durante el sueño.
            elif (90 <= spo2 <= 93) or (105 < ritmo <= 130) or (40 <= ritmo < 50) or (temperatura > 37.8) or (movimiento in ["agitado", "movimiento frecuente"]):
                estado = "inestable"
                tipo_alerta = "alta"
                
                if 90 <= spo2 <= 93:
                    alerta_texto = f"Alerta Alta: Hipoxia moderada en reposo (SpO2: {spo2}%)."
                    recomendacion = "⚠️ Observación: Oxígeno por debajo del estándar óptimo. Verifique vías aéreas y postura del adulto mayor."
                else:
                    alerta_texto = "Alerta Alta: Constantes inestables o agitación física."
                    recommendacion = "⚠️ Monitoreo continuo: Paciente inestable o con movimientos nocturnos inusuales."

            # 🟡 ALERTA LEVE (Fluctuación fisiológica aceptable)
            # - Ritmo cardíaco ligeramente elevado (101 - 105 lpm) o actividad motriz leve.
            elif (100 < ritmo <= 105) or (movimiento == "leve"):
                estado = "alerta"
                tipo_alerta = "media"
                alerta_texto = "Alerta Leve: Frecuencia cardíaca ligeramente elevada o actividad menor."
                recomendacion = "Descanso recomendado. Evaluar microdespertar nocturno."

        # ========================================================
        # HISTORIAL GENERAL Y CONTROL DE SPAM DE ALERTAS
        # ========================================================
        
        # Guardado en el historial de signos vitales (RegistroSalud)
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

        # Evitar duplicados consecutivos de alertas en la base de datos (Intervalo de 30 segundos)
        crear_alerta = True
        ultima_alerta = Alerta.objects.filter(paciente=paciente).order_by("-fecha_hora").first()
        if ultima_alerta and (timezone.now() - ultima_alerta.fecha_hora < timedelta(seconds=30)):
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
            "recomendacion": recomendacion,
            "bateria_recibida": bateria
        })

    except Exception as e:
        return Response({"success": False, "message": f"Error interno del servidor: {str(e)}"})


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

    alertas = Alerta.objects.filter(paciente_id=paciente_id).order_by("-fecha_hora")[:10]

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