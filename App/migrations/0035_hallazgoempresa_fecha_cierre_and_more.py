# Generated by Django 5.1.3 on 2025-01-27 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0034_alter_comunicacionhallazgo_hallazgo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hallazgoempresa',
            name='fecha_cierre',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalhallazgoempresa',
            name='fecha_cierre',
            field=models.DateField(blank=True, null=True),
        ),
    ]
