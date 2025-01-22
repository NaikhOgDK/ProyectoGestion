# Generated by Django 5.1.3 on 2025-01-22 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_delete_asignacionvehiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_retiro', models.DateField()),
                ('patente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.vehiculo')),
                ('taller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.group')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaAsignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('Aceptada', 'Aceptada'), ('Rechazada', 'Rechazada')], max_length=10)),
                ('comentario_rechazo', models.TextField(blank=True, null=True)),
                ('fecha_respuesta', models.DateTimeField(auto_now_add=True)),
                ('asignacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='App.asignacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
