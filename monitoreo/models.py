from django.db import models
from django.utils import timezone


# =========================
# PACIENTE
# =========================
class Paciente(models.Model):
    nombres = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    codigo_qr = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombres


# =========================
# USUARIO
# =========================
class Usuario(models.Model):
    nombres = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombres


# =========================
# RELACIÓN PACIENTE - USUARIO
# =========================
class PacienteUsuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    relacion = models.CharField(max_length=50)
    permiso_alertas = models.BooleanField(default=True)


# =========================
# DISPOSITIVO
# =========================
class Dispositivo(models.Model):
    codigo_pulsera = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20)
    fecha_activacion = models.DateField(default=timezone.now)
    activo = models.BooleanField(default=True)


# =========================
# ASIGNACIÓN DISPOSITIVO
# =========================
class AsignacionDispositivo(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)


# =========================
# SESIÓN DE SUEÑO
# =========================
class SesionSueno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Sesion {self.paciente.nombres}"


# =========================
# REGISTRO DE SALUD (SENSORES)
# =========================
class RegistroSalud(models.Model):
    sesion = models.ForeignKey(SesionSueno, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)

    ritmo_cardiaco = models.IntegerField()
    spo2 = models.IntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=2)

    # 🔥 MPU6050 / MOVIMIENTO
    movimiento = models.CharField(max_length=50, default="estable")

    # ALERTAS
    alerta = models.BooleanField(default=False)
    tipo_alerta = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Registro {self.sesion.paciente.nombres} - {self.fecha_hora}"


# =========================
# ALERTA MÉDICA
# =========================
class Alerta(models.Model):
    ESTADOS = [
        ("normal", "Normal"),
        ("alerta", "Alerta"),
        ("critico", "Crítico"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=timezone.now)

    tipo_alerta = models.CharField(max_length=100)
    descripcion = models.TextField()

    estado = models.CharField(max_length=50, choices=ESTADOS, default="normal")

    def __str__(self):
        return f"{self.paciente.nombres} - {self.estado}"


# =========================
# CONFIRMACIÓN ALERTA
# =========================
class ConfirmacionAlerta(models.Model):
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    fecha_hora = models.DateTimeField(default=timezone.now)
    accion = models.CharField(max_length=50)

    def __str__(self):
        return f"Confirmación {self.usuario.nombres}"