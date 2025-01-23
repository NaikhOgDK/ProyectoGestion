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
from django.views.generic import ListView
from django.utils import timezone
import requests
from decouple import config
from django.http import JsonResponse

@login_required
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
                response = HttpResponse()
                # Set token in cookies
                token = user.role.name  # Aquí deberías obtener el token real
                response.set_cookie('auth_token', token, httponly=True, secure=True)

                # Redirect based on role
                if user.role.name == 'Administrador':
                    response['Location'] = 'home'
                elif user.role.name == 'Visualizador':
                    response['Location'] = 'homeVisual'
                elif user.role.name == 'Empresa':
                    response['Location'] = 'homeEmpresa'
                elif user.role.name == 'Taller':
                    response['Location'] = 'homeTallerUsuario'
                else:
                    messages.error(request, "Role not defined for this user.")
                    return render(request, 'acceso/login.html', {'form': form})

                response.status_code = 302
                return response
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
    return user.role and user.role.name == "Administrador"

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

def crear_asignacion(request):
    if request.method == 'POST':
        form = AsignacionVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homeTaller')  # Cambia por tu vista de redirección
    else:
        form = AsignacionVehiculoForm()
    return render(request, 'areas/taller/crear_asignacion.html', {'form': form})

class UnidadAceptadaListView(ListView):
    model = UnidadAceptada
    template_name = 'areas/taller/unidad_aceptada_list.html'  # Archivo de plantilla para la lista
    context_object_name = 'unidades'  # Nombre de la variable en el contexto
    
    def get_queryset(self):
        # Si deseas filtrar las unidades aceptadas por el taller del usuario, puedes hacerlo aquí
        if self.request.user.group:
            return UnidadAceptada.objects.filter(taller=self.request.user.group)
        return UnidadAceptada.objects.all()

def unidades_pendientes(request):
    unidades = UnidadAceptada.objects.filter(estado='Pendiente')
    return render(request, 'areas/taller/unidades_pendientes.html', {'unidades': unidades})

def unidades_en_proceso(request):
    unidades = UnidadAceptada.objects.filter(estado='En Proceso')
    return render(request, 'areas/taller/unidades_en_proceso.html', {'unidades': unidades})

def unidades_reparadas(request):
    unidades = UnidadAceptada.objects.filter(estado='Reparada')
    return render(request, 'areas/taller/unidades_reparadas.html', {'unidades': unidades})

def marcar_como_reparada(request, unidad_id):
    # Asegúrate de que la unidad existe
    unidad = UnidadAceptada.objects.get(id=unidad_id)
    
    # Actualiza el estado de la unidad a "Reparada"
    unidad.estado = 'Reparada'
    unidad.save()
    
    # Redirige de vuelta a la página de unidades reparadas
    return redirect('unidades_reparadas')

def chat_view(request):
    groups = Group.objects.all()
    selected_group_id = request.GET.get('group_id')
    selected_group = Group.objects.get(id=selected_group_id) if selected_group_id else None
    messages = Message.objects.filter(group=selected_group).order_by('timestamp') if selected_group else []

    if request.method == 'POST':
        content = request.POST.get('content')
        group_id = request.POST.get('group_id')
        if content and group_id:
            group = Group.objects.get(id=group_id)
            Message.objects.create(
                sender=request.user,
                group=group,
                content=content,
                timestamp=timezone.now()
            )
            return redirect('chat')  # Redirigir para evitar reenvío de formulario

    return render(request, 'chat/chat.html', {'groups': groups, 'messages': messages, 'selected_group': selected_group})

#Fin Taller Admin

#Chat

def admin_chat_view(request):
    if not request.user.role or request.user.role.name != 'Administrador':
        return redirect('user_chat')  # Redirigir a la vista de usuario si no es admin

    groups = Group.objects.all()
    selected_group_id = request.GET.get('group_id')
    selected_group = Group.objects.get(id=selected_group_id) if selected_group_id else None
    messages = Message.objects.filter(group=selected_group).order_by('timestamp') if selected_group else []

    if request.method == 'POST':
        content = request.POST.get('content')
        group_id = request.POST.get('group_id')
        if content and group_id:
            group = Group.objects.get(id=group_id)
            Message.objects.create(
                sender=request.user,
                group=group,
                content=content,
                timestamp=timezone.now()
            )
            return redirect('admin_chat')  # Redirigir para evitar reenvío de formulario

    return render(request, 'chat/admin_chat.html', {'groups': groups, 'messages': messages, 'selected_group': selected_group})

def user_chat_view(request):
    user_group = request.user.group
    messages = Message.objects.filter(group=user_group).order_by('timestamp') if user_group else []

    if request.method == 'POST':
        content = request.POST.get('content')
        if content and user_group:
            Message.objects.create(
                sender=request.user,
                group=user_group,
                content=content,
                timestamp=timezone.now()
            )
            return redirect('user_chat')  # Redirigir para evitar reenvío de formulario

    return render(request, 'chat/user_chat.html', {'messages': messages, 'user_group': user_group})

#Fin Chat

#Inicio Taller usuario

def listar_asignaciones(request):
    # Obtener todas las asignaciones sin aplicar filtros
    asignaciones = Asignacion_taller.objects.all()

    return render(request, 'areas/taller/listar_asignaciones.html', {'asignaciones': asignaciones})


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
    grupo_usuario = request.user.group

    if grupo_usuario:
        asignaciones = Asignacion_taller.objects.filter(taller=grupo_usuario)
    else:
        asignaciones = Asignacion_taller.objects.none()

    if request.method == 'POST':
        asignacion_id = request.POST.get('asignacion_id')
        estado = request.POST.get('estado')
        comentario_rechazo = request.POST.get('comentario_rechazo', '')
        fecha_retiro = request.POST.get('fecha_retiro', '')
        comentario = request.POST.get('comentario', '')

        asignacion = get_object_or_404(Asignacion_taller, id=asignacion_id)

        if estado == 'Aceptada':
            if not fecha_retiro or not comentario:
                messages.error(request, "Debe proporcionar todos los campos requeridos.")
                return redirect('gestionar_asignaciones')

            # Crear respuesta de asignación
            RespuestaAsignacion_taller.objects.create(
                asignacion=asignacion,
                usuario=request.user,
                estado=estado,
                comentario_rechazo='',
                fecha_retiro=fecha_retiro,
                comentario=comentario,
            )

            # Crear registro en UnidadAceptada
            UnidadAceptada.objects.create(
                patente=asignacion.patente,
                taller=asignacion.taller,
                fecha_respuesta=asignacion.respuestas.last().fecha_respuesta,
                fecha_retiro=fecha_retiro,
            )

            messages.success(request, "Asignación aceptada correctamente.")

        elif estado == 'Rechazada':
            if not comentario_rechazo:
                messages.error(request, "Debe proporcionar un motivo para rechazar la asignación.")
                return redirect('gestionar_asignaciones')

            RespuestaAsignacion_taller.objects.create(
                asignacion=asignacion,
                usuario=request.user,
                estado=estado,
                comentario_rechazo=comentario_rechazo,
            )
            messages.success(request, "Asignación rechazada correctamente.")

        return redirect('gestionar_asignaciones')

    return render(request, 'taller/gestionar_asignaciones.html', {'asignaciones': asignaciones})

def lista_unidades_aceptadas(request):
    # Obtener el grupo (taller) del usuario actual
    grupo_usuario = request.user.group
    
    # Filtrar las unidades aceptadas por el taller asignado al usuario
    if grupo_usuario:
        unidades_aceptadas = UnidadAceptada.objects.filter(taller=grupo_usuario)
    else:
        unidades_aceptadas = UnidadAceptada.objects.none()

    return render(request, 'taller/lista_unidades.html', {'unidades_aceptadas': unidades_aceptadas})

def editar_unidad_aceptada(request, unidad_id):
    # Obtener la unidad aceptada específica
    unidad = get_object_or_404(UnidadAceptada, id=unidad_id)

    # Verificar que el usuario pertenece al taller (grupo) de la unidad
    if request.user.group != unidad.taller:
        return redirect('unauthorized_access')  # Redirigir si no pertenece al grupo

    # Crear el formulario con los datos actuales de la unidad
    if request.method == 'POST':
        form = UnidadAceptadaForm(request.POST, request.FILES, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('lista_unidades_aceptadas')  # Redirigir a la lista de unidades aceptadas
    else:
        form = UnidadAceptadaForm(instance=unidad)

    return render(request, 'taller/editar_unidad.html', {'form': form, 'unidad': unidad})
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

#API

def make_post_request(request):
    token = request.COOKIES.get('auth_token')
    if token == 'Administrador':
        url = 'https://www.drivetech.pro/api/v1/get_vehicles_positions/'
        tokengps = config('API_TOKEN')
        headers = {
            'Authorization': f'Token {tokengps}',
            'Content-Type': 'application/json'
        }
        body = {
            'client_id': 'coca-cola_andina'
        }

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            return JsonResponse({'status': 'success', 'data': response.json()})
        else:
            return JsonResponse({'status': 'error', 'message': response.text}, status=response.status_code)
    else:
        return JsonResponse({'status': 'error', 'message': 'Usuario no Autenticado'}, status=404)

#Fin API