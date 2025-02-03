from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError
from django.contrib.auth import get_user_model  # Usar el modelo User configurado
from .models import UsuarioEmpresa, UsuarioTaller  # Importar los modelos correspondientes

User = get_user_model()  # Obtener el modelo User correcto

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Solo ejecuta si el usuario es recién creado
        if instance.role and instance.role.name == 'Empresa':  # Si el rol es "Empresa"
            try:
                # Crear un UsuarioEmpresa
                UsuarioEmpresa.objects.create(user=instance, grupo=instance.group)
            except IntegrityError:
                # Evitar duplicados si ya existe un perfil asociado
                pass
        elif instance.role and instance.role.name == 'Taller':  # Si el rol es "Taller"
            try:
                # Crear un UsuarioTaller
                UsuarioTaller.objects.create(user=instance, grupo=instance.group)
            except IntegrityError:
                # Evitar duplicados si ya existe un perfil asociado
                pass
