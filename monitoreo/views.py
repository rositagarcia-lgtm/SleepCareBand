from rest_framework import viewsets
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