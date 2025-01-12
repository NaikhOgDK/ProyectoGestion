from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    def __str__(self):
        return self.username

#Modelo Vehiculos
class Vehiculo(models.Model):
    patente = models.CharField(max_length=20)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    nro_motor = models.CharField(max_length=50)
    nro_chasis = models.CharField(max_length=50)
    tipo_vehiculo = models.CharField(max_length=50)
    nro_pallets = models.IntegerField()
    tipo_carroceria = models.CharField(max_length=50)
    seccion = models.CharField(max_length=50)
    ubicacion_fisica = models.CharField(max_length=100)
    propietario = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    operacion = models.CharField(max_length=50)
    empresa = models.CharField(max_length=100)
    transportista = models.CharField(max_length=100)
    observacion = models.TextField()

    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo}"

#Modelo Documento
class Documento(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)

    Mantencion_Preventiva = models.FileField(upload_to='documentos/', blank=True, null=True)
    fecha_vencimiento_mantencion = models.DateField(blank=True, null=True)  # Fecha de vencimiento para Mantención Preventiva
    
    Revision_Tecnica = models.FileField(upload_to='documentos/', blank=True, null=True)
    fecha_vencimiento_revision = models.DateField(blank=True, null=True)  # Fecha de vencimiento para Revisión Técnica
    
    Permiso_Circulacion = models.FileField(upload_to='documentos/', blank=True, null=True)
    fecha_vencimiento_permiso = models.DateField(blank=True, null=True)  # Fecha de vencimiento para Permiso de Circulación
    
    SOAP = models.FileField(upload_to='documentos/', blank=True, null=True)
    fecha_vencimiento_soap = models.DateField(blank=True, null=True)  # Fecha de vencimiento para SOAP
    
    Padron = models.FileField(upload_to='documentos/', blank=True, null=True)
    fecha_vencimiento_padron = models.DateField(blank=True, null=True)  # Fecha de vencimiento para Padrón
    
    descripcion = models.TextField(blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vehiculo.patente if self.vehiculo else 'Documento sin vehículo'

#Modelo Mnatenimiento
class Mantenimiento(models.Model):
    SERVICIOS_CHOICES = [
        ('SM1', 'SM1'),
        ('SM2', 'SM2'),
        ('SM3', 'SM3'),
        ('SM4', 'SM4'),
    ]
    
    PROXIMO_SERVICIO_CHOICES = [
        ('SM1', 'SM1'),
        ('SM2', 'SM2'),
        ('SM3', 'SM3'),
        ('SM4', 'SM4'),
    ]
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True)  # Permite borrar el vehículo, pero mantiene el mantenimiento
    kilometraje_mtto = models.IntegerField()  # Kilometraje al momento del mantenimiento
    fecha_mtto = models.DateField()  # Fecha del mantenimiento
    servicio_realizado = models.CharField(max_length=3, choices=SERVICIOS_CHOICES)  # Opciones de servicio realizado
    respaldo_mtto = models.FileField(upload_to='mantenimientos/', blank=True, null=True)  # Respaldo del mantenimiento (como archivo)
    proximo_mantenimiento_km = models.IntegerField()  # Kilometraje para el próximo mantenimiento
    proximo_servicio = models.CharField(max_length=3, choices=PROXIMO_SERVICIO_CHOICES)  # Opciones para el próximo servicio

    def __str__(self):
        # Verificamos si el vehículo existe antes de intentar acceder a la patente
        if self.vehiculo:
            return f"Mantenimiento de {self.vehiculo.patente} - {self.fecha_mtto}"
        else:
            return f"Mantenimiento sin vehículo asociado - {self.fecha_mtto}"


class HistorialMantenimiento(models.Model):
    mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.DO_NOTHING)  # El historial no se borra al eliminar mantenimiento
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Fecha y hora en que se registró el historial
    kilometraje_mtto = models.IntegerField()  # Kilometraje al momento del mantenimiento
    servicio_realizado = models.CharField(max_length=3, choices=Mantenimiento.SERVICIOS_CHOICES)
    respaldo_mtto = models.FileField(upload_to='historial_mantenimientos/', blank=True, null=True)
    proximo_mantenimiento_km = models.IntegerField()  # Kilometraje para el próximo mantenimiento
    proximo_servicio = models.CharField(max_length=3, choices=Mantenimiento.PROXIMO_SERVICIO_CHOICES)  # Proximo servicio

    def __str__(self):
        # Verificamos si el vehículo existe antes de intentar acceder a la patente
        if self.mantenimiento.vehiculo:
            return f"Historial de mantenimiento de {self.mantenimiento.vehiculo.patente} - {self.fecha_registro}"
        else:
            return f"Historial de mantenimiento sin vehículo asociado - {self.fecha_registro}"

# Señal para crear historial cuando se guarda un nuevo mantenimiento
@receiver(post_save, sender=Mantenimiento)
def crear_historial_mantenimiento(sender, instance, created, **kwargs):
    if created:
        # Crear un nuevo historial con los datos del mantenimiento recién creado
        HistorialMantenimiento.objects.create(
            mantenimiento=instance,
            kilometraje_mtto=instance.kilometraje_mtto,
            servicio_realizado=instance.servicio_realizado,
            respaldo_mtto=instance.respaldo_mtto,
            proximo_mantenimiento_km=instance.proximo_mantenimiento_km,
            proximo_servicio=instance.proximo_servicio,
        )

