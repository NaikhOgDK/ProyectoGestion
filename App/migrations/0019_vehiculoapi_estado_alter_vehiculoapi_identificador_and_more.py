# Generated by Django 5.1.3 on 2025-01-23 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0018_alter_vehiculoapi_identificador'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculoapi',
            name='estado',
            field=models.CharField(choices=[('online', 'Online'), ('offline', 'Offline')], default='offline', max_length=10),
        ),
        migrations.AlterField(
            model_name='vehiculoapi',
            name='identificador',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculoapi',
            name='placa',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
