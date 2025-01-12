from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
import pandas as pd
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'acceso/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on role
                if user.role.name == 'Admin':
                    return redirect('home')
                elif user.role.name == 'Visualizador':
                    return redirect('home')
                elif user.role.name == 'Empresa':
                    return redirect('homeEmpresa')
                else:
                    messages.error(request, "Role not defined for this user.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'acceso/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, "acceso/logout.html")

#Carga Informacion
def cargar_datos_excel(request):
    # Ruta del archivo Excel
    archivo = 'C:/Users/Nicolas Vilches/OneDrive - OCA ENSAYOS INSPECCIONES Y CERTIFICACIONES CHILE S.A/Proyecto Koandina/Koandina BBDD.xlsx'

    # Leer solo la hoja llamada 'Base'
    df_base = pd.read_excel(archivo, sheet_name='Base')

    # Contador para llevar registro de los registros nuevos
    registros_creados = 0

    # Iterar sobre las filas del DataFrame
    for _, row in df_base.iterrows():
        # Verificar si ya existe un registro con la misma patente
        if not Vehiculo.objects.filter(patente=row['Patente']).exists():
            # Si no existe, crear el nuevo registro
            Vehiculo.objects.create(
                patente=row['Patente'],
                marca=row['Marca'],
                modelo=row['Modelo'],
                ano=row['Año'],
                nro_motor=row['N° de motor'],
                nro_chasis=row['N° Chasis'],
                tipo_vehiculo=row['Tipo Vehiculo'],
                nro_pallets=row['N° de pallets'],
                tipo_carroceria=row['Tipo carrocería'],
                seccion=row['Sección'],
                ubicacion_fisica=row['Ubicación fisica'],
                propietario=row['Propietario'],
                tipo=row['Tipo'],
                operacion=row['Operación'],
                empresa=row['Empresa'],
                transportista=row['Transportista'],
                observacion=row['Observacion']
            )
            registros_creados += 1

    # Devolver una respuesta indicando el número de registros cargados
    return HttpResponse(f"Datos cargados correctamente. Nuevos registros creados: {registros_creados}")

#Seccion home Admin
def home(request):
    return render(request,'home.html')

def homeNeumatico(request):
    return render(request, 'areas/neumatico/homeneu.html')

def homeGPS(request):
    return render(request, 'areas/gps/homegps.html')

def homeDocumentacion(request):
    return render(request, 'areas/documento/homedoc.html')

def homeTaller(request):
    return render(request, 'areas/taller/hometaller.html')
#fin Admin

#Documentacion
def Documentos(request): 
    # Obtener los valores de búsqueda y filtro
    query = request.GET.get('search', '')  # Búsqueda por patente
    tipo_filtro = request.GET.get('tipo', '')  # Filtro por tipo

    # Filtrar los vehículos
    vehiculos = Vehiculo.objects.all()
    if query:
        vehiculos = vehiculos.filter(patente__icontains=query)
    if tipo_filtro:
        vehiculos = vehiculos.filter(tipo=tipo_filtro)

    # Opciones de tipo para el filtro
    tipos = [
        ('Operativo', 'Operativo'),
        ('No Disponible', 'No Disponible'),
        ('En Taller', 'En Taller'),
        ('En Venta', 'En Venta'),
        ('Fuera de Servicio', 'Fuera de Servicio'),
    ]

    # Pasar los datos y filtros actuales a la plantilla
    return render(request, 'areas/documento/listadoc.html', {
        'vehiculos': vehiculos,
        'search': query,
        'tipo_filtro': tipo_filtro,
        'tipos': tipos,
    })

def cargar_documentos(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            # Asignar el vehículo actual al formulario
            documento = form.save(commit=False)
            documento.vehiculo = vehiculo
            documento.save()
            return redirect('Documentos')  # Redirige después de guardar el documento
    else:
        form = DocumentoForm()

    return render(request, 'areas/documento/cargar_documentos.html', {
        'vehiculo': vehiculo,
        'form': form
    })

#Fin Documentacion
def homeEmpresa(request):
    return render(request,'empresa/home.html')

