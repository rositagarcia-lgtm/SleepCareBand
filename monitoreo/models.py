from django.db import models


class Paciente(models.Model):
    nombres = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    codigo_qr = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombres


class Usuario(models.Model):
    nombres = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombres


class PacienteUsuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    relacion = models.CharField(max_length=50)
    permiso_alertas = models.BooleanField(default=True)


class Dispositivo(models.Model):
    codigo_pulsera = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20)
    fecha_activacion = models.DateField()
    activo = models.BooleanField(default=True)


class AsignacionDispositivo(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)


class SesionSueno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()


class RegistroSalud(models.Model):
    sesion = models.ForeignKey(SesionSueno, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    ritmo_cardiaco = models.IntegerField()
    spo2 = models.IntegerField()
    temperatura = models.DecimalField(max_digits=4, decimal_places=2)
    movimiento = models.CharField(max_length=50)
    alerta = models.BooleanField(default=False)
    tipo_alerta = models.CharField(max_length=100, null=True, blank=True)


class Alerta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    tipo_alerta = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50)


class ConfirmacionAlerta(models.Model):
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    accion = models.CharField(max_length=50)