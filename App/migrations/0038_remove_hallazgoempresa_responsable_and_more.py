# Generated by Django 5.1.3 on 2025-02-03 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0037_alter_vehiculo_empresa_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hallazgoempresa',
            name='responsable',
        ),
        migrations.RemoveField(
            model_name='historicalhallazgoempresa',
            name='responsable',
        ),
    ]
