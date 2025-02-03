from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    #Seccion acceso
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_user, name="logout"),
    #Fin acceso

    #Seccion Admin
    path('home/', views.home, name="home"),
    path('Neumatico', views.homeNeumatico, name="homeNeumatico"),
    path('GPS', views.homeGPS, name="homeGPS"),
    path('Documento', views.homeDocumentacion, name="homeDocumentacion"),
    path('Taller', views.homeTaller, name="homeTaller"),
    path('visual', views.visual, name="visual"),
    path('homeVisual', views.homeVisual, name="homeVisual"),
    #Fin Admin

    #Consulta
    path('consulta/', views.consulta_vehiculo, name='consulta_vehiculo'),
    path('detalle/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    #Fin Consulta

    #Asigancion
    path('asignar-empresa/', asignar_empresa, name='asignar_empresa'),
    #Fin Asignacion

    #Carga Datos
    path('cargar-datos/', cargar_datos_excel, name='cargar_datos_excel'),
    #Fin Carga Datos

    # GPS

    path('vehiculos-seguimiento/', views.get_vehiculos_con_seguimiento, name='vehiculos_seguimiento'),

    #Fin GPS

    # URLS Documentos
    path('Documentos/', views.Documentos, name='Documentos'),
    path('documentos/cargar/<int:id>/', views.cargar_documentos, name='cargar_documentos'),
    path('editar_documentos/<int:id>/', views.editar_documentos, name='editar_documentos'),
    path('crear_mantenimiento/', views.crear_mantenimiento, name='crear_mantenimiento'),
    path('listado_vehiculos/', views.listado_vehiculos, name='listado_vehiculos'),
    path('vehiculos/historial/<int:vehiculo_id>/', views.historial_vehiculo, name='historial_mantenimiento'),
    # Fin Urls Documentos

    # URLS Neumaticos
    path('empresa/hallazgos/', views.listar_hallazgo, name='listar_hallazgo'),
    path('hallazgo/close/<int:hallazgo_id>/', views.cerrar_hallazgoemp, name='hallazgo_close'),
    path('cerrar-hallazgo/<int:pk>/', views.cerrar_hallazgo, name='cerrar_hallazgo'),
    path('hallazgo/<int:hallazgo_id>/', views.detalle_hallazgoemp, name='detalle_hallazgoemp'),
    path('hallazgo/reabrir/<int:hallazgo_id>/', views.reabrir_hallazgo, name='hallazgo_reabrir'),
    path('hallazgo/add_comunicacion/<int:hallazgo_id>/', views.add_comunicacion, name='add_comunicacion'),
    # Fin URLS Nuematicos

    #Empresa Hallazgo

    #Fin Empresa Hallazgo

    #Inicio Empresa
    path('homeEmpresa/', views.homeEmpresa, name="homeEmpresa"),
    path('Mis_Vehiculos', views.vehiculos_del_grupo, name="vehiculos_del_grupo"),
    path('vehiculos/<int:vehiculo_id>/cargar_documentos/', views.cargar_documentosemp, name='cargar_documentosemp'),
    path('vehiculos/<int:vehiculo_id>/editar_documentos/', views.editar_documentosemp, name='editar_documentosemp'),
    path('lista_vehiculosdoc', views.lista_documentos, name='lista_documentos'),
    #Fin Empresa

    #Servicio Chat
    path('chat/', views.chat_view, name='chat'),
    path('admin_chat/', views.admin_chat_view, name='admin_chat'),
    path('user_chat/', views.user_chat_view, name='user_chat'),
    #Fin Chat

    #Taller Admin
    path('crear_asignacion/', views.crear_asignacion, name='crear_asignacion'),
    path('unidades/pendientes/', views.unidades_pendientes, name='unidades_pendientes'),
    path('unidades/en_proceso/', views.unidades_en_proceso, name='unidades_en_proceso'),
    path('unidades/reparadas/', views.unidades_reparadas, name='unidades_reparadas'),
    path('marcar-como-reparada/<int:unidad_id>/', views.marcar_como_reparada, name='marcar_como_reparada'),
    path('unidad-aceptada/', views.unidad_aceptada_list, name='unidad_aceptada_list'),
    path('listar/mantencion-reparacion/', views.listar_mantencion_reparacion, name='listar_mantencion_reparacion'),
    path('listar/asignaciones-empresa/', views.listar_asignaciones_empresa, name='listar_asignaciones_empresa'),
    #Fin Taller Admin

    #Taller Usuario
    path('homeTallerUsuario', views.homeTallerUsuario, name="homeTallerUsuario"),
    path('listar_asignaciones/', views.listar_asignaciones, name='listar_asignaciones'),
    path('actualizar_estado/<int:asignacion_id>/', views.actualizar_estado, name='actualizar_estado'),
    path('gestionar_asignaciones/', views.gestionar_asignaciones, name='gestionar_asignaciones'),
    path('lista-unidades/', views.lista_unidades_aceptadas, name='lista_unidades_aceptadas'),
    path('editar-unidad/<int:unidad_id>/', views.editar_unidad_aceptada, name='editar_unidad'),
    #Fin Taller Usuario

    #API

    path('api/make_post_request/', make_post_request, name='make_post_request'),

    #Fin API

    #Desempeño

    path('dashboard/', views.dashboard_view, name='dashboard'),

    #Fin Desempeño

    path('listar_hallazgoemp/', views.listar_hallazgoemp, name='listar_hallazgoemp'),
    path('crear_hallazgo/', views.crear_hallazgo, name='crear_hallazgo'),
    path('hallazgo/<int:hallazgo_id>/', views.detalle_hallazgo, name='detalle_hallazgo'),
    path('hallazgo/cerrar/<int:hallazgo_id>/', views.cerrar_hallazgo, name='cerrar_hallazgo'),
    path('hallazgo/detalle/<int:hallazgo_id>/', views.detalle_hallazgo, name='detalle_hallazgo'),

    path('permission-denied/', permission_denied_view, name='permission_denied'),

    #Vista AC Comercial

    path('homeACComercial', views.homeACComercial, name='homeACComercial'),

    #Fin Vista AC Comercial

]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
