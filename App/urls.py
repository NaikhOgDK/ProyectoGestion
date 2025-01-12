from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    #Fin Admin

    #Consulta
    path('consulta/', views.consulta_vehiculo, name='consulta_vehiculo'),
    path('detalle/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    #Fin Consulta

    #Carga Datos
    path('cargar_datos_excel/', views.cargar_datos_excel, name='cargar_datos_excel'),
    #Fin Carga Datos

    # URLS Documentos
    path('Documentos/', views.Documentos, name='Documentos'),
    path('documentos/cargar/<int:id>/', views.cargar_documentos, name='cargar_documentos'),
    path('crear_mantenimiento/', views.crear_mantenimiento, name='crear_mantenimiento'),
    path('listado_vehiculos/', views.listado_vehiculos, name='listado_vehiculos'),
    path('vehiculos/historial/<int:vehiculo_id>/', views.historial_vehiculo, name='historial_mantenimiento'),
    # Fin Urls Documentos

    path('homeEmpresa/', views.homeEmpresa, name="homeEmpresa"),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
