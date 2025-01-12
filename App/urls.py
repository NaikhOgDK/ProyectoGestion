from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('home/', views.home, name="home"),
    path('homeEmpresa/', views.homeEmpresa, name="homeEmpresa"),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('visualizer-dashboard/', views.visualizer_dashboard, name='visualizer_dashboard'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
]
