from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('visualizer-dashboard/', views.visualizer_dashboard, name='visualizer_dashboard'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
]
