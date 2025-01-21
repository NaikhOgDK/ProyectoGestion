from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Group)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Vehiculo)
admin.site.register(Documento)
admin.site.register(Mantenimiento)
admin.site.register(HistorialMantenimiento)
admin.site.register(AsignacionVehiculo)