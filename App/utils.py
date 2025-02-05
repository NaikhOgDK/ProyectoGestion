from django.core.mail import send_mail
import boto3
from django.conf import settings

def enviar_notificacion_grupo(hallazgo, asunto, mensaje, tipo='creacion'):
    """
    Función para enviar una notificación por correo a todos los miembros de un grupo
    cuando se crea o se cierra un hallazgo.
    """
    miembros_grupo = hallazgo.grupo.users.all()  # Usar el 'related_name' correcto para acceder a los usuarios
    correos = [user.email for user in miembros_grupo]  # Obtener los correos electrónicos de los miembros
    
    if tipo == 'creacion':
        # Mensaje para la creación de un hallazgo
        mensaje_detallado = f"""
        Se ha creado un nuevo hallazgo:

        Descripción: {hallazgo.hallazgo}
        Fecha de inspección: {hallazgo.fecha_inspeccion}
        Tipo: {hallazgo.tipo_hallazgo}
        Responsable: {hallazgo.responsable.user.username}
        """
    
    elif tipo == 'cierre':
        # Mensaje para el cierre de un hallazgo
        cierre = hallazgo.cierre
        mensaje_detallado = f"""
        Se ha cerrado un hallazgo:

        Descripción: {hallazgo.hallazgo}
        Fecha de inspección: {hallazgo.fecha_inspeccion}
        Tipo: {hallazgo.tipo_hallazgo}
        Responsable: {hallazgo.responsable.user.username}

        Cierre del Hallazgo:
        Descripción: {cierre.descripcion_cierre}
        Responsable de Cierre: {cierre.responsable_cierre.user.username if cierre.responsable_cierre else 'No asignado'}
        """
    
    # Enviar el correo
    send_mail(asunto, mensaje_detallado, 'nicolasvilchesa12@gmail.com', correos)


def upload_file_to_s3(local_file, s3_file_name):
    """
    Subir un archivo a un bucket de AWS S3.

    :param local_file: Ruta del archivo en el sistema local.
    :param s3_file_name: Nombre del archivo en el bucket S3.
    :return: True si la carga fue exitosa, False si hubo un error.
    """
    try:
        # Crear un cliente de S3 con las credenciales
        s3_client = boto3.client(
            service_name='s3',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        )

        # Realizar la carga del archivo
        s3_client.upload_file(local_file, settings.AWS_STORAGE_BUCKET_NAME, s3_file_name)
        print(f"Archivo {local_file} subido correctamente a {s3_file_name} en S3.")
        return True
    except Exception as e:
        print(f"Error al subir archivo a S3: {e}")
        return False
