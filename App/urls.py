from django.urls import path
from . import views

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
    
    path('homeEmpresa/', views.homeEmpresa, name="homeEmpresa"),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('visualizer-dashboard/', views.visualizer_dashboard, name='visualizer_dashboard'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
]
