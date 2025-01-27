from django.core.mail import send_mail

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

