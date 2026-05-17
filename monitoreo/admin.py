from django.contrib import admin
from .models import *

admin.site.register(Paciente)
admin.site.register(Usuario)
admin.site.register(PacienteUsuario)
admin.site.register(Dispositivo)
admin.site.register(AsignacionDispositivo)
admin.site.register(SesionSueno)
admin.site.register(RegistroSalud)
admin.site.register(Alerta)
admin.site.register(ConfirmacionAlerta)