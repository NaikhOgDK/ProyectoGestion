# Generated by Django 5.1.3 on 2025-01-24 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_camion_carroceria_empresa_microempresa_operacion_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Camion',
            new_name='Vehiculo',
        ),
    ]
