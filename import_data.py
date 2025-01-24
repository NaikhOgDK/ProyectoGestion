import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from App.models import (
    Marca, TipoVehiculo, Carroceria, Canal, Zona, Seccion, ubicacion_fisica, Propietario, Operacion, Empresa, Microempresa, Vehiculo
)

# Ruta al archivo Excel
file_path = 'C:/Users/Nicolas Vilches/OneDrive - OCA ENSAYOS INSPECCIONES Y CERTIFICACIONES CHILE S.A/Proyecto Koandina/Koandina BBDD.xlsx'

# Cargar el archivo Excel con pandas
data = pd.read_excel(file_path)

# Iterar por cada fila del archivo Excel
for _, row in data.iterrows():
    try:
        # Crear o buscar objetos relacionados
        marca, _ = Marca.objects.get_or_create(nombre=row["Marca"])
        tipo_vehiculo, _ = TipoVehiculo.objects.get_or_create(tipo=row["Tipo Vehiculo"])
        carroceria, _ = Carroceria.objects.get_or_create(nombre=row["Tipo carrocería"])
        canal, _ = Canal.objects.get_or_create(canal=row["Canal"])
        zona, _ = Zona.objects.get_or_create(zona=row["Zona"])
        seccion, _ = Seccion.objects.get_or_create(nombre=row["Sección"])
        ubicacion, _ = ubicacion_fisica.objects.get_or_create(nombre=row["Ubicación fisica"])
        propietario, _ = Propietario.objects.get_or_create(tipo_propietario=row["Propietario"])
        operacion, _ = Operacion.objects.get_or_create(operacion=row["Operación"])
        empresa, _ = Empresa.objects.get_or_create(nombre=row["Empresa"])
        
        # Si es una microempresa, crearla o buscarla
        es_microempresa = pd.notna(row["Transportista"]) and row["Transportista"] != "N/A"
        microempresa = None
        if es_microempresa:
            microempresa, _ = Microempresa.objects.get_or_create(nombre=row["Transportista"])

        # Crear el vehículo
        Vehiculo.objects.create(
            patente=row["Patente"],
            marca=marca,
            modelo=row["Modelo"],
            ano=row["Año"],
            num_motor=row["N° de motor"],
            num_chasis=row["N° Chasis"],
            num_pallets=row["N° de pallets"],
            tipo_vehiculo=tipo_vehiculo,
            carroceria=carroceria,
            canal=canal,
            zona=zona,
            seccion=seccion,
            ubicacion_fisica=ubicacion,
            propietario=propietario,
            operacion=operacion,
            empresa=empresa,
            es_microempresa=es_microempresa,
            microempresa=microempresa,
        )
        print(f"Vehículo {row['Patente']} cargado con éxito.")
    except Exception as e:
        print(f"Error al cargar el vehículo con patente {row['Patente']}: {e}")
