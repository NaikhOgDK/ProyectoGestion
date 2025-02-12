# Generated by Django 5.1.3 on 2025-01-12 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_alter_vehiculo_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Procedimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('archivo', models.FileField(upload_to='procedimientos/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('area', models.CharField(choices=[('Documentacion', 'Documentación'), ('GPS', 'GPS'), ('Neumatico', 'Neumático'), ('Taller', 'Taller')], max_length=50)),
            ],
        ),
    ]
