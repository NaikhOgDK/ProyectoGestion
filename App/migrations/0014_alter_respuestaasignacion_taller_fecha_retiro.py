# Generated by Django 5.1.3 on 2025-01-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_asignacion_taller_respuestaasignacion_taller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuestaasignacion_taller',
            name='fecha_retiro',
            field=models.DateField(blank=True, null=True),
        ),
    ]
