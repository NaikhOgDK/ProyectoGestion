from django.contrib import admin
from .models import *
from .utils import enviar_notificacion_grupo
# Register your models here.

admin.site.register(Group)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Vehiculo)
admin.site.register(Documento)
admin.site.register(Mantenimiento)
admin.site.register(HistorialMantenimiento)
admin.site.register(Asignacion_taller)
admin.site.register(UnidadAceptada)
admin.site.register(VehiculoAPI)
admin.site.register(UsuarioEmpresa)
admin.site.register(UsuarioTaller)
admin.site.register(Tipo)
admin.site.register(tipo_usuario)
admin.site.register(HistoricalVehiculo)
admin.site.register(EstadoGPS)
admin.site.register(HallazgoEmpresa)
admin.site.register(Cierre)
admin.site.register(HistoricalHallazgoEmpresa)
admin.site.register(Message)