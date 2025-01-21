from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import *
from .models import *
import pandas as pd
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

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
                    return redirect('homeVisual')
                elif user.role.name == 'Empresa':
                    return redirect('homeEmpresa')
                elif user.role.name == 'Taller':
                    return redirect('homeTallerUsuario')
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

def visual(request):
    return render(request, 'areas/visual/visual.html')
#Fin Admin

#Consulta
def consulta_vehiculo(request):
    query = request.GET.get('search', '')
    
    # Filtrar vehículos por patente, marca o modelo
    vehiculos = Vehiculo.objects.filter(
        Q(patente__icontains=query) | Q(marca__icontains=query) | Q(modelo__icontains=query)
    )
    
    context = {
        'vehiculos': vehiculos,
        'search': query
    }
    return render(request, 'Consulta/consulta.html', context)

def detalle_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    documentos = Documento.objects.filter(vehiculo=vehiculo)
    hallazgos = Hallazgo.objects.filter(vehiculo=vehiculo)
    mantenimientos = Mantenimiento.objects.filter(vehiculo=vehiculo)
    reparaciones = Reparacion.objects.filter(vehiculo=vehiculo)
    
    context = {
        'vehiculo': vehiculo,
        'documentos': documentos,
        'hallazgos': hallazgos,
        'mantenimientos': mantenimientos,
        'reparaciones': reparaciones
    }
    return render(request, 'Consulta/detalle_vehiculo.html', context)
#Fin Consulta

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

    for vehiculo in vehiculos:
        vehiculo.documentos_count = vehiculo.documento_set.count()
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

def editar_documentos(request, id):
    # Obtén el vehículo específico por su ID
    vehiculo = get_object_or_404(Vehiculo, id=id)

    # Obtén los documentos asociados al vehículo
    documentos = Documento.objects.filter(vehiculo=vehiculo)

    # Si no existe ningún documento, redirigir o mostrar un mensaje
    if not documentos:
        return redirect('cargar_documentos', id=id)  # Redirigir a cargar documentos

    # Si el formulario se ha enviado
    if request.method == 'POST':
        for documento in documentos:
            form = DocumentoForm(request.POST, request.FILES, instance=documento)
            if form.is_valid():
                form.save()  # Guarda los cambios del documento
        return redirect('Documentos')  # Redirige a la lista de vehículos (ajusta la ruta según tu proyecto)

    # Si no se ha enviado el formulario, mostrar el formulario de edición
    context = {
        'vehiculo': vehiculo,
        'documentos': documentos,
    }
    return render(request, 'areas/documento/editar_documentos.html', context)

def crear_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homeDocumentacion')  # Redirige a una lista de mantenimientos o cualquier otra vista
    else:
        search = request.GET.get('search', '')
        form = MantenimientoForm()

        if search:
            form.fields['vehiculo'].queryset = Vehiculo.objects.filter(patente__icontains=search)
    
    return render(request, 'areas/documento/crear_mantenimiento.html', {'form': form})

def listado_vehiculos(request):
    # Obtener el término de búsqueda
    search = request.GET.get('search', '')
    
    # Filtrar vehículos por patente si existe la búsqueda
    if search:
        vehiculos = Vehiculo.objects.filter(patente__icontains=search)
    else:
        vehiculos = Vehiculo.objects.all()

    return render(request, 'areas/documento/lista_vehiculos.html', {
        'vehiculos': vehiculos,
        'search': search,
    })

def historial_vehiculo(request, vehiculo_id):
    # Obtener el vehículo seleccionado
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    # Obtener el historial de mantenimientos asociados a ese vehículo
    historial = HistorialMantenimiento.objects.filter(mantenimiento__vehiculo=vehiculo).order_by('-fecha_registro')

    return render(request, 'areas/documento/historial_vehiculo.html', {
        'vehiculo': vehiculo,
        'historial': historial,
    })

#Fin Documentacion

#Inicio Neumatico

# Verificar si el usuario es analista (Admin)
def is_analyst(user):
    return user.role and user.role.name == "Admin"

# Verificar si el usuario es parte de una empresa
def is_company(user):
    return user.role and user.role.name == "Empresa"

# Lista de hallazgos
@login_required
def hallazgo_list(request):
    if is_analyst(request.user):
        hallazgos = Hallazgo.objects.all()  # Analistas ven todos los hallazgos
    elif is_company(request.user):
        hallazgos = Hallazgo.objects.filter(grupo=request.user.group)  # Empresas ven solo los de su grupo
    else:
        hallazgos = Hallazgo.objects.none()
    return render(request, "areas/neumatico/hallazgo_list.html", {"hallazgos": hallazgos})

# Crear o editar hallazgo (solo analistas)
@login_required
@user_passes_test(is_analyst)
def hallazgo_create_or_edit(request, pk=None):
    hallazgo = get_object_or_404(Hallazgo, pk=pk) if pk else None
    if request.method == "POST":
        form = HallazgoForm(request.POST, request.FILES, instance=hallazgo)
        if form.is_valid():
            form.save()
            return redirect("hallazgo_list")
    else:
        form = HallazgoForm(instance=hallazgo)
    return render(request, "areas/neumatico/hallazgo_form.html", {"form": form, "hallazgo": hallazgo})

# Cerrar/Reabrir hallazgo (Empresas y analistas)
@login_required
def hallazgo_close_or_reopen(request, pk):
    hallazgo = get_object_or_404(Hallazgo, pk=pk)
    if is_company(request.user) and hallazgo.grupo != request.user.group:
        return redirect("hallazgo_list")  # Empresas solo pueden cerrar los suyos
    if request.method == "POST":
        if hallazgo.estado_cierre == "Abierto":
            hallazgo.estado_cierre = "Cerrado"
        else:
            hallazgo.estado_cierre = "Abierto"
        hallazgo.save()
        return redirect("hallazgo_detail", pk=pk)
    return render(request, "areas/neumatico/hallazgo_close.html", {"hallazgo": hallazgo})

# Ver detalles del hallazgo
@login_required
def hallazgo_detail(request, pk):
    hallazgo = get_object_or_404(Hallazgo, pk=pk)
    comunicaciones = hallazgo.comunicacionhallazgo_set.all()
    return render(request, "areas/neumatico/hallazgo_detail.html", {"hallazgo": hallazgo, "comunicaciones": comunicaciones})

# Agregar comunicación
@login_required
def add_comunicacion(request, hallazgo_pk):
    hallazgo = get_object_or_404(Hallazgo, pk=hallazgo_pk)
    if request.method == "POST":
        form = ComunicacionForm(request.POST, request.FILES)
        if form.is_valid():
            comunicacion = form.save(commit=False)
            comunicacion.hallazgo = hallazgo
            comunicacion.usuario = request.user
            comunicacion.save()
            return redirect("hallazgo_detail", pk=hallazgo.pk)
    else:
        form = ComunicacionForm()
    return render(request, "areas/neumatico/comunicacion_form.html", {"form": form, "hallazgo": hallazgo})
#Fin Neumatico

#Empresa Hallazgo

@login_required
def empresa_hallazgos(request):
    # Obtener el grupo del usuario autenticado
    grupo_usuario = request.user.group  # Suponiendo que el usuario pertenece a un único grupo
    if not grupo_usuario:
        return render(request, 'empresa/hallazgos_list.html', {'hallazgos': [], 'grupo': None})
    
    # Filtrar los hallazgos del grupo del usuario
    hallazgos = Hallazgo.objects.filter(grupo__name=grupo_usuario.name).order_by('-fecha_inspeccion')
    
    # Paginación (10 hallazgos por página)
    paginator = Paginator(hallazgos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'empresa/hallazgos_list.html', {
        'hallazgos': page_obj,
        'grupo': grupo_usuario
    })

@login_required
def cerrar_hallazgo(request, pk):
    hallazgo = get_object_or_404(Hallazgo, pk=pk)

    if request.method == 'POST':
        form = HallazgoCierreForm(request.POST, request.FILES, instance=hallazgo)
        if form.is_valid():
            hallazgo.estado_cierre = 'Cerrado'
            form.save()
            messages.success(request, "El hallazgo ha sido cerrado exitosamente.")
            return redirect('empresa_hallazgos')
    else:
        form = HallazgoCierreForm(instance=hallazgo)

    return render(request, 'empresa/cerrar_hallazgo.html', {'form': form, 'hallazgo': hallazgo})

def detalle_hallazgo(request, pk):
    hallazgo = get_object_or_404(Hallazgo, pk=pk)

    if request.method == "POST":
        # Si se ha enviado el formulario de comunicación
        form = ComunicacionForm(request.POST, request.FILES)
        if form.is_valid():
            comunicacion = form.save(commit=False)
            comunicacion.hallazgo = hallazgo
            comunicacion.usuario = request.user
            comunicacion.save()
            # Redirigir de nuevo al detalle del hallazgo para que se vea la nueva comunicación
            return redirect('detalle_hallazgo', pk=hallazgo.pk)
    else:
        # Si es una petición GET, solo creamos el formulario vacío
        form = ComunicacionForm()

    return render(request, 'empresa/detalle_hallazgo.html', {'hallazgo': hallazgo, 'form': form})

#Fin Empresa Hallazgo

#Inicio Taller Admin

def asignar_vehiculos(request):
    if request.method == "POST":
        form = AsignacionVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homeTaller')
    else:
        form = AsignacionVehiculoForm()
    return render(request, 'areas/taller/asignar_vehiculos.html', {'form': form})

#Fin Taller Admin

#Inicio Taller usuario

def listar_asignaciones(request):
    taller = request.user.group  # El taller del usuario
    asignaciones = AsignacionVehiculo.objects.filter(taller=taller)
    return render(request, 'taller/listar_asignaciones.html', {'asignaciones': asignaciones})

def actualizar_estado(request, asignacion_id):
    asignacion = AsignacionVehiculo.objects.get(id=asignacion_id)
    if request.method == "POST":
        form = ActualizarEstadoForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            return redirect('listar_asignaciones')
    else:
        form = ActualizarEstadoForm(instance=asignacion)
    return render(request, 'taller/actualizar_estado.html', {'form': form, 'asignacion': asignacion})

def gestionar_asignaciones(request):
    # Filtrar asignaciones relacionadas con el taller del usuario
    asignaciones = AsignacionVehiculo.objects.filter(taller=request.user.group)

    if request.method == 'POST':
        # Procesar la actualización de las asignaciones
        asignaciones_ids = request.POST.getlist('asignaciones_seleccionadas[]')  # IDs seleccionadas
        for asignacion_id in asignaciones_ids:
            try:
                asignacion = AsignacionVehiculo.objects.get(id=asignacion_id)
                nuevo_estado = request.POST.get(f'estado_{asignacion_id}')
                motivo = request.POST.get(f'motivo_{asignacion_id}', '')

                # Actualizar campos
                asignacion.estado = nuevo_estado
                asignacion.comentario_rechazo = motivo if nuevo_estado == 'Rechazada' else ''
                asignacion.save()
            except AsignacionVehiculo.DoesNotExist:
                continue

        messages.success(request, "Asignaciones actualizadas correctamente.")
        return redirect('gestionar_asignaciones')  # Vuelve a la misma vista

    # Renderizar la plantilla con las asignaciones
    return render(request, 'taller/gestionar_asignaciones.html', {'asignaciones': asignaciones})

#Fin Taller Usuario

#Vista Empresa
def homeEmpresa(request):
    return render(request,'empresa/home.html')
#Fin Vista Empresa

#Vista Visualizador
def homeVisual(request):
    return render(request, 'visualizador/homevi.html')
#Fin Vista Visualizador

#Vista Taller
def homeTallerUsuario(request):
    return render(request, 'taller/hometaller.html')
#Fin Vista Taller