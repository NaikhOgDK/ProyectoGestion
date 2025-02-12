# Generated by Django 5.1.3 on 2025-02-03 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0038_remove_hallazgoempresa_responsable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hallazgoempresa',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.usuarioempresa'),
        ),
        migrations.AddField(
            model_name='historicalhallazgoempresa',
            name='responsable',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.usuarioempresa'),
        ),
    ]
