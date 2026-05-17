from rest_framework import serializers
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


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"


class PacienteUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteUsuario
        fields = "__all__"


class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = "__all__"


class AsignacionDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionDispositivo
        fields = "__all__"


class SesionSuenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionSueno
        fields = "__all__"


class RegistroSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroSalud
        fields = "__all__"


class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = "__all__"


class ConfirmacionAlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmacionAlerta
        fields = "__all__"
        