from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from django.utils import timezone

class Group(models.Model):
    TIPO_GRUPO = [
        ('taller', 'Taller'),
        ('empresa', 'Empresa'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    tipo_grupo = models.CharField(max_length=10, choices=TIPO_GRUPO, default='taller')  # Indica si es taller o empresa
    
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

class tipo_usuario(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return selp.nombre

class UsuarioEmpresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    # Agregar los campos adicionales que necesites para los usuarios Empresa

    def __str__(self):
        return f"{self.user.username} - {self.user.group}"

class UsuarioTaller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    # Agregar los campos adicionales que necesites para los usuarios Taller

    def __str__(self):
        return f"{self.user.username} - {self.user.group}"

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
class Tipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Carroceria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    zona = models.CharField(max_length=50)

    def __str__(self):
        return self.zona

class Canal(models.Model):
    canal = models.CharField(max_length=50)

    def __str__(self):
        return self.canal

class ubicacion_fisica(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre

class Propietario(models.Model):
    tipo_propietario = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo_propietario

class Operacion(models.Model):
    operacion = models.CharField(max_length=50)

    def __str__(self):
        return self.operacion

class Microempresa(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
        
class TipoVehiculo(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo
 
class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)  # Nueva clave foránea a Marca
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    num_motor = models.CharField(max_length=50)
    num_chasis = models.CharField(max_length=50)
    num_pallets = models.IntegerField()

    # Relaciones
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.SET_NULL, null=True, blank=True)
    carroceria = models.ForeignKey(Carroceria, on_delete=models.SET_NULL, null=True, blank=True)
    zona = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True)
    ubicacion_fisica = models.ForeignKey(ubicacion_fisica, on_delete=models.SET_NULL, null=True, blank=True)
    seccion = models.ForeignKey(Seccion, on_delete=models.SET_NULL, null=True, blank=True)
    propietario = models.ForeignKey(Propietario, on_delete=models.SET_NULL, null=True, blank=True)
    empresa = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    operacion = models.ForeignKey(Operacion, on_delete=models.SET_NULL, null=True, blank=True)
    canal = models.ForeignKey(Canal, on_delete=models.SET_NULL, null=True, blank=True)
    microempresa = models.ForeignKey(Microempresa, on_delete=models.SET_NULL, null=True, blank=True)

    # Campo booleano para saber si es microempresa
    es_microempresa = models.BooleanField(default=False)
    history = HistoricalRecords()  # Agregar historial

    def clean(self):
        # Validación para asegurar que solo se asocie una microempresa si es_microempresa es True
        if self.es_microempresa and not self.microempresa:
            raise ValidationError("Debe asociarse una microempresa si el vehículo pertenece a una microempresa.")
        elif not self.es_microempresa and self.microempresa:
            raise ValidationError("No debe asociarse una microempresa si el vehículo no pertenece a una microempresa.")

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"


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
    history = HistoricalRecords()  # Agregar historial

    def __str__(self):
        return self.vehiculo.patente if self.vehiculo else 'Documento sin vehículo'

class imagenDocumentos(models.Model):
    imagen = models.FileField(upload_to='ImagenesDoc', blank=True, null=True)
        

class Conductor(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15)
    FechaVencimientoLicencia = models.DateField()
    empresa = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class LicenciaConductor(models.Model):
    conductor = models.ForeignKey(Conductor, related_name="licencias", on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='licencias', null=True, blank=True)  # Puede ser imagen o PDF

    def __str__(self):
        return f"Licencia de {self.conductor.nombre} ({self.id})"

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

#Prueba hallazgo nuevo

class HallazgoEmpresa(models.Model):
    TIPO_HALLAZGO_CHOICES = [
        ('Neumático', 'Neumático'),
        ('Surco', 'Surco'),
    ]
    RIESGO_CHOICES = [
        ('Alto', 'Alto'),
        ('Medio', 'Medio'),
        ('Bajo', 'Bajo'),
    ]
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Cerrado', 'Cerrado'),
    ]

    hallazgo = models.CharField(max_length=255)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el vehículo
    posicion_neumatico = models.CharField(max_length=50, choices=[(f'P{i}', f'P{i}') for i in range(1, 11)])  # P1, P2, ..., P10
    fecha_inspeccion = models.DateField()
    tipo_hallazgo = models.CharField(max_length=50, choices=TIPO_HALLAZGO_CHOICES)
    nivel_riesgo = models.CharField(max_length=10, choices=RIESGO_CHOICES)
    responsable = models.ForeignKey(UsuarioEmpresa, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el responsable
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el grupo (empresa)
    evidencia = models.FileField(upload_to='evidencias/', null=True, blank=True)  # Evidencia (foto o PDF)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')  # Estado del hallazgo
    fecha_cierre = models.DateField(null=True, blank=True)  # Fecha de cierre del hallazgo

    # Historial
    history = HistoricalRecords()  # Si deseas mantener un historial de cambios

    def cerrar_hallazgo(self):
        """Método para cerrar un hallazgo cambiando su estado a 'Cerrado' y estableciendo la fecha de cierre."""
        self.estado = 'Cerrado'
        self.fecha_cierre = timezone.now().date()  # Establece la fecha de cierre como la fecha actual
        self.save()  # Guarda el hallazgo con el nuevo estado y fecha de cierre

    @property
    def dias_para_cerrar(self):
        """Método para calcular los días transcurridos entre la fecha de inspección y la fecha de cierre."""
        if self.estado == 'Cerrado' and self.fecha_cierre:
            return (self.fecha_cierre - self.fecha_inspeccion).days
        return None  # Si no está cerrado o falta la fecha de cierre, retorna None

    @property
    def clasificacion_tiempo_cierre(self):
        """Clasifica el tiempo de cierre del hallazgo como Efectivo, Regular o Ineficiente."""
        dias = self.dias_para_cerrar
        if dias is not None:
            if dias <= 2:
                return 'Efectivo'
            elif 3 <= dias <= 5:
                return 'Regular'
            else:
                return 'Ineficiente'
        return 'No cerrado'  # Si el hallazgo no está cerrado aún

    def __str__(self):
        return f"{self.hallazgo} ({self.tipo_hallazgo} - {self.nivel_riesgo})"


class Cierre(models.Model):
    hallazgo = models.OneToOneField(HallazgoEmpresa, on_delete=models.CASCADE)  # Relación uno a uno con el hallazgo
    responsable_cierre = models.ForeignKey(UsuarioEmpresa, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsable_cierre')
    descripcion_cierre = models.TextField(null=True, blank=True)  # Descripción del trabajo realizado
    evidencia_cierre = models.FileField(upload_to='cierres/', null=True, blank=True)  # Evidencia del cierre
    documento_cierre = models.FileField(upload_to='documentos_cierre/', null=True, blank=True)  # Documento de cierre

    def save(self, *args, **kwargs):
        """Al guardar un cierre, cambia el estado del hallazgo relacionado a 'Cerrado' y guarda la fecha de cierre."""
        super().save(*args, **kwargs)
        if self.hallazgo.estado != 'Cerrado':
            self.hallazgo.cerrar_hallazgo()

    def __str__(self):
        return f"Cierre del Hallazgo {self.hallazgo.id} - {self.hallazgo.estado}"
        

class ComunicacionHallazgo(models.Model):
    hallazgo = models.ForeignKey(HallazgoEmpresa, on_delete=models.SET_NULL, null=True)  # Relación con el hallazgo
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Usuario que envía la comunicación
    mensaje = models.TextField()  # Mensaje del usuario sobre el hallazgo
    fecha_envio = models.DateTimeField(auto_now_add=True)  # Fecha de envío del mensaje
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Respondido', 'Respondido')], default='Pendiente')  # Estado de la comunicación
    evidencia_adicional = models.FileField(upload_to='comunicaciones_hallazgos/', null=True, blank=True)  # Evidencia adicional (foto, documento, etc.)

    def __str__(self):
        return f"Comunicacion del Hallazgo {self.hallazgo.id} por {self.usuario.username} - {self.estado}"

#Fin Prueba hallazgo nuevo

#Taller

class Reparacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el vehículo
    taller = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con el taller
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

class Asignacion_taller(models.Model):
    TIPOS_ASIGNACION = [
        ('mantencion_preventiva', 'Mantención Preventiva'),
        ('mantencion_correctiva', 'Mantención Correctiva'),
        ('reparacion', 'Reparación'),
        ('asignacion_empresa', 'Asignación Empresa'),
    ]

    patente = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)  # Vehículo asignado
    taller = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="talleres")  # Grupo (taller) asignado
    fecha_asignacion = models.DateTimeField(auto_now_add=True)  # Fecha de asignación
    motivo = models.TextField()  # Motivo de la asignación
    tipo = models.CharField(max_length=30, choices=TIPOS_ASIGNACION, default='Mantención Preventiva')  # Tipo de asignación

    # Campos para Mantención o Reparación
    fecha_disponible_mantencion = models.DateField(null=True, blank=True)  # Fecha en que la unidad estará disponible para mantenimiento
    descripcion_tarea = models.TextField(null=True, blank=True)  # Descripción de la tarea (si es mantenimiento o reparación)


    # Campos para Asignación Empresa
    empresa_asignada = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="empresas")  # Empresa asignada (si es asignación empresa)
    fecha_disponible_asignacion = models.DateField(null=True, blank=True)  # Fecha en que la unidad estará disponible para asignación
    descripcion_asignacion = models.TextField(null=True, blank=True)  # Descripción de lo que se debe hacer en la asignación

    def __str__(self):
        return f"{self.patente} asignado a {self.taller.name} - Tipo: {self.tipo}"

class RespuestaAsignacion_taller(models.Model):
    asignacion = models.ForeignKey(Asignacion_taller, on_delete=models.CASCADE, related_name='respuestas')  # Relación con la asignación
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que responde (miembro del grupo)
    estado = models.CharField(
        max_length=10,
        choices=[('Aceptada', 'Aceptada'), ('Rechazada', 'Rechazada')],
    )  
    # Estado de la respuesta
    comentario_rechazo = models.TextField(blank=True, null=True)  # Motivo en caso de rechazo
    fecha_respuesta = models.DateTimeField(auto_now_add=True)  # Fecha de la respuesta

    #Comentario accepta
    fecha_retiro = models.DateField(blank=True, null=True)
    comentario = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - {self.estado} - {self.asignacion}"

class UnidadAceptada(models.Model):
    patente = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)  # Vehículo
    taller = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)  # Taller
    fecha_respuesta = models.DateTimeField()  # Fecha en que se aceptó la asignación
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Reparada', 'Reparada')],
        default='Pendiente'
    )  # Estado del proceso
    fecha_retiro = models.DateField()  # Fecha de retiro proporcionada al aceptar la asignación
    fecha_inicio = models.DateField(blank=True, null=True)  # Fecha de inicio de reparación
    fecha_termino = models.DateField(blank=True, null=True)  # Fecha de término de reparación
    kilometraje = models.PositiveIntegerField(blank=True, null=True)  # Kilometraje del vehículo
    registro = models.FileField(upload_to='ot_reparacion/', blank=True, null=True)  # Documento OT de reparación
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Costo total

    class Meta:
        verbose_name_plural = "Unidades Aceptadas"
        ordering = ['fecha_respuesta']

    def __str__(self):
        return f"{self.patente} - {self.taller.name} - {self.estado}"

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Este campo indica si el mensaje ha sido leído

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

#GPS        

class VehiculoAPI(models.Model):
    placa = models.CharField(max_length=100)
    identificador = models.CharField(max_length=100, null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    fecha_hora = models.DateTimeField(null=True, blank=True)
    odometro = models.FloatField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='api_data',null=True, blank=True)

    def __str__(self):
        return f"{self.placa} - {self.estado}"


class EstadoGPS(models.Model):
    ESTADO_CHOICES = [
        ('Sin GPS', 'Sin GPS'),
        ('Pendiente Instalación', 'Pendiente Instalación'),
        ('Instalado', 'Instalado'),
    ]

    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, related_name='estado_gps')
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='Sin GPS')
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vehículo {self.vehiculo.patente}: {self.estado}"
    
    history = HistoricalRecords()

@receiver(post_save, sender=Vehiculo)
def crear_estado_gps(sender, instance, created, **kwargs):
    if created:
        EstadoGPS.objects.create(vehiculo=instance)

#Fin GPS


#Mantenimiento



#Fin Mantenimiento