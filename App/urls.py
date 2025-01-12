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
    #Carga Datos
    path('cargar_datos_excel/', views.cargar_datos_excel, name='cargar_datos_excel'),
    #Fin Carga Datos
    # URLS Documentos
    path('Documentos/', views.Documentos, name='Documentos'),
    path('documentos/cargar/<int:id>/', views.cargar_documentos, name='cargar_documentos'),
    # Fin Urls Documentos
    path('homeEmpresa/', views.homeEmpresa, name="homeEmpresa"),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
