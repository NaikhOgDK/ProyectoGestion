# Generated by Django 5.1.3 on 2025-01-27 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0030_hallazgoempresa_cierre_historicalhallazgoempresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioempresa',
            name='grupo',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='App.group'),
            preserve_default=False,
        ),
    ]
