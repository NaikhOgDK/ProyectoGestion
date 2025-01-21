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

#Procedimiento
class Procedimiento(models.Model):
    # Definimos las opciones para el campo 'area'
    AREA_CHOICES = [
        ('Documentacion', 'Documentación'),
        ('GPS', 'GPS'),
        ('Neumatico', 'Neumático'),
        ('Taller', 'Taller'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='procedimientos/')  # Asegúrate de que la carpeta de carga esté configurada
    fecha_subida = models.DateTimeField(auto_now_add=True)
    area = models.CharField(max_length=50, choices=AREA_CHOICES)  # Agregado el campo 'area'

    def __str__(self):
        return self.nombre

#Modelo Vehiculos
class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('Operativo', 'Operativo'),
        ('No Disponible', 'No Disponible'),
        ('En Taller', 'En Taller'),
        ('En Venta', 'En Venta'),
        ('Fuera de Servicio', 'Fuera de Servicio'),
    ]
    
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
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)  # Usando choices para limitar las opciones
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


#Modelo Mantenimiento
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

#Modelo Hallazgo
class Hallazgo(models.Model):
    TIPO_HALLAZGO_CHOICES = [
        ('Neumático', 'Neumático'),
        ('Surco', 'Surco'),
    ]
    RIESGO_CHOICES = [
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo'),
    ]
    CIERRE_CHOICES = [
        ('Abierto', 'Abierto'),
        ('Cerrado', 'Cerrado'),
    ]

    hallazgo = models.CharField(max_length=255)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el vehículo (patente)
    posicion_neumatico = models.CharField(max_length=50, choices=[(f'P{i}', f'P{i}') for i in range(1, 11)])  # P1, P2, ..., P10
    fecha_inspeccion = models.DateField()
    tipo_hallazgo = models.CharField(max_length=50, choices=TIPO_HALLAZGO_CHOICES)
    nivel_riesgo = models.CharField(max_length=10, choices=RIESGO_CHOICES)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el responsable
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el grupo (empresa)
    evidencia = models.FileField(upload_to='evidencias/', null=True, blank=True)  # Evidencia (foto o PDF)

    # Cierre
    estado_cierre = models.CharField(max_length=10, choices=CIERRE_CHOICES, default='Abierto')
    responsable_cierre = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsable_cierre')
    descripcion_cierre = models.TextField(null=True, blank=True)  # Descripción del trabajo realizado
    evidencia_cierre = models.FileField(upload_to='cierres/', null=True, blank=True)  # Evidencia del cierre
    documento_cierre = models.FileField(upload_to='documentos_cierre/', null=True, blank=True)  # Documento de cierre

    def __str__(self):
        return f"{self.hallazgo} ({self.tipo_hallazgo} - {self.estado_cierre})"


class ComunicacionHallazgo(models.Model):
    hallazgo = models.ForeignKey(Hallazgo, on_delete=models.SET_NULL, null=True)  # Relación con el hallazgo
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Usuario que envía la comunicación
    mensaje = models.TextField()  # Mensaje del usuario sobre el hallazgo
    fecha_envio = models.DateTimeField(auto_now_add=True)  # Fecha de envío del mensaje
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Respondido', 'Respondido')], default='Pendiente')  # Estado de la comunicación
    evidencia_adicional = models.FileField(upload_to='comunicaciones_hallazgos/', null=True, blank=True)  # Evidencia adicional (foto, documento, etc.)

    def __str__(self):
        return f"Comunicacion del Hallazgo {self.hallazgo.id} por {self.usuario.username} - {self.estado}"

#Taller
class Taller(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del taller
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección del taller
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Teléfono del taller
    encargado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario encargado del taller
    usuarios = models.ManyToManyField(User, related_name='talleres', blank=True)  # Relación Many-to-Many con los usuarios

    def __str__(self):
        return f"Taller: {self.nombre}"

class Reparacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el vehículo
    taller = models.ForeignKey(Taller, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el taller
    kilometraje = models.IntegerField()  # Kilometraje al momento de la reparación
    fecha_inicio = models.DateField()  # Fecha de inicio de la reparación
    fecha_termino = models.DateField()  # Fecha de término de la reparación
    registro = models.FileField(upload_to='reparaciones/', blank=True, null=True)  # Registro de la reparación (documento)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2)  # Costo total de la reparación
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Reparada', 'Reparada')])  # Estado de la reparación

    def __str__(self):
        return f"Reparación de {self.vehiculo.patente if self.vehiculo else 'Sin vehículo'} - Taller: {self.taller.nombre if self.taller else 'Sin taller'}"

class ComunicacionReparacion(models.Model):
    reparacion = models.ForeignKey(Reparacion, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con la reparación
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que envía la comunicación
    mensaje = models.TextField()  # Mensaje del usuario sobre la reparación
    fecha_envio = models.DateTimeField(auto_now_add=True)  # Fecha de envío del mensaje
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Respondido', 'Respondido')], default='Pendiente')  # Estado de la comunicación
    evidencia_adicional = models.FileField(upload_to='comunicaciones_reparaciones/', null=True, blank=True)  # Evidencia adicional (foto, documento, etc.)

    def __str__(self):
        return f"Comunicacion de Reparación {self.reparacion.id} por {self.usuario.username} - {self.estado}"

class AsignacionVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)  # Relación con vehículo
    empresa = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='asignaciones')  # Empresa que asigna
    fecha_asignacion = models.DateField(auto_now_add=True)  # Fecha de asignación
    estado = models.CharField(
        max_length=50,
        choices=[('Pendiente', 'Pendiente'), ('Aceptada', 'Aceptada'), ('Rechazada', 'Rechazada')],
        default='Pendiente'
    )  # Estado de asignación
    comentario_rechazo = models.TextField(blank=True, null=True)  # Comentario en caso de rechazo

    def __str__(self):
        return f"{self.vehiculo.patente} - {self.taller.nombre} - {self.estado}"

