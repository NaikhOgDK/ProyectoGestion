# Generated by Django 5.1.3 on 2025-01-27 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0031_usuarioempresa_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariotaller',
            name='grupo',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='App.group'),
            preserve_default=False,
        ),
    ]
