# Generated by Django 5.1.3 on 2025-01-27 12:33

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0026_tipo_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='imagenDocumentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.FileField(blank=True, null=True, upload_to='ImagenesDoc')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalDocumento',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('Mantencion_Preventiva', models.TextField(blank=True, max_length=100, null=True)),
                ('fecha_vencimiento_mantencion', models.DateField(blank=True, null=True)),
                ('Revision_Tecnica', models.TextField(blank=True, max_length=100, null=True)),
                ('fecha_vencimiento_revision', models.DateField(blank=True, null=True)),
                ('Permiso_Circulacion', models.TextField(blank=True, max_length=100, null=True)),
                ('fecha_vencimiento_permiso', models.DateField(blank=True, null=True)),
                ('SOAP', models.TextField(blank=True, max_length=100, null=True)),
                ('fecha_vencimiento_soap', models.DateField(blank=True, null=True)),
                ('Padron', models.TextField(blank=True, max_length=100, null=True)),
                ('fecha_vencimiento_padron', models.DateField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha_subida', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('vehiculo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.vehiculo')),
            ],
            options={
                'verbose_name': 'historical documento',
                'verbose_name_plural': 'historical documentos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalHallazgo',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('hallazgo', models.CharField(max_length=255)),
                ('posicion_neumatico', models.CharField(choices=[('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3'), ('P4', 'P4'), ('P5', 'P5'), ('P6', 'P6'), ('P7', 'P7'), ('P8', 'P8'), ('P9', 'P9'), ('P10', 'P10')], max_length=50)),
                ('fecha_inspeccion', models.DateField()),
                ('tipo_hallazgo', models.CharField(choices=[('Neumático', 'Neumático'), ('Surco', 'Surco')], max_length=50)),
                ('nivel_riesgo', models.CharField(choices=[('Alto', 'Alto'), ('Medio', 'Medio'), ('Bajo', 'Bajo')], max_length=10)),
                ('evidencia', models.TextField(blank=True, max_length=100, null=True)),
                ('estado_cierre', models.CharField(choices=[('Abierto', 'Abierto'), ('Cerrado', 'Cerrado')], default='Abierto', max_length=10)),
                ('descripcion_cierre', models.TextField(blank=True, null=True)),
                ('evidencia_cierre', models.TextField(blank=True, max_length=100, null=True)),
                ('documento_cierre', models.TextField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('grupo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.group')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('responsable', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('responsable_cierre', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('vehiculo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.vehiculo')),
            ],
            options={
                'verbose_name': 'historical hallazgo',
                'verbose_name_plural': 'historical hallazgos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalVehiculo',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('patente', models.CharField(db_index=True, max_length=10)),
                ('modelo', models.CharField(max_length=100)),
                ('ano', models.IntegerField()),
                ('num_motor', models.CharField(max_length=50)),
                ('num_chasis', models.CharField(max_length=50)),
                ('num_pallets', models.IntegerField()),
                ('es_microempresa', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('canal', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.canal')),
                ('carroceria', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.carroceria')),
                ('empresa', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.empresa')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('marca', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.marca')),
                ('microempresa', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.microempresa')),
                ('operacion', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.operacion')),
                ('propietario', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.propietario')),
                ('seccion', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.seccion')),
                ('tipo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.tipo')),
                ('tipo_vehiculo', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.tipovehiculo')),
                ('ubicacion_fisica', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.ubicacion_fisica')),
                ('zona', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='App.zona')),
            ],
            options={
                'verbose_name': 'historical vehiculo',
                'verbose_name_plural': 'historical vehiculos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
