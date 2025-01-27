from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UsuarioEmpresa, UsuarioTaller

@receiver(post_save, sender=User)
def assign_user_to_role(sender, instance, created, **kwargs):
    if created:
        if instance.role.name == 'Empresa':
            # Crea el usuario en el modelo UsuarioEmpresa y asigna el grupo
            UsuarioEmpresa.objects.create(user=instance, grupo=instance.group)
        elif instance.role.name == 'Taller':
            # Crea el usuario en el modelo UsuarioTaller y asigna el grupo
            UsuarioTaller.objects.create(user=instance, grupo=instance.group)