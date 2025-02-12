# Generated by Django 5.1.3 on 2025-02-13 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0045_alter_hallazgoempresa_responsable_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hallazgoempresa',
            name='responsable',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='J', to='App.usuarioempresa'),
        ),
        migrations.AlterField(
            model_name='historicalhallazgoempresa',
            name='responsable',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.usuarioempresa'),
        ),
    ]
