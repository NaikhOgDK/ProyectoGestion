# Generated by Django 5.1.3 on 2025-01-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0035_hallazgoempresa_fecha_cierre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
