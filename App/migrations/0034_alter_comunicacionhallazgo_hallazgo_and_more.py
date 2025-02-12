# Generated by Django 5.1.3 on 2025-01-27 19:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0033_remove_cierre_estado_cierre_hallazgoempresa_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comunicacionhallazgo',
            name='hallazgo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.hallazgoempresa'),
        ),
        migrations.RemoveField(
            model_name='historicalhallazgo',
            name='grupo',
        ),
        migrations.RemoveField(
            model_name='historicalhallazgo',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalhallazgo',
            name='responsable',
        ),
        migrations.RemoveField(
            model_name='historicalhallazgo',
            name='responsable_cierre',
        ),
        migrations.RemoveField(
            model_name='historicalhallazgo',
            name='vehiculo',
        ),
        migrations.DeleteModel(
            name='Hallazgo',
        ),
        migrations.DeleteModel(
            name='HistoricalHallazgo',
        ),
    ]
