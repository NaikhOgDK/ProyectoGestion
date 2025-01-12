from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import Role

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
                    return redirect('admin_dashboard')
                elif user.role.name == 'Visualizador':
                    return redirect('visualizer_dashboard')
                elif user.role.name == 'Empresa':
                    return redirect('company_dashboard')
                else:
                    messages.error(request, "Role not defined for this user.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'acceso/login.html', {'form': form})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def visualizer_dashboard(request):
    return render(request, 'visualizer_dashboard.html')

@login_required
def company_dashboard(request):
    return render(request, 'company_dashboard.html')
