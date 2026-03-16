from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Wallet


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Wallet.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}. Tu wallet fue creada.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegisterForm()
    
    return render(request, 'wallet/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido de vuelta, {user.username}.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'wallet/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente.')
        return redirect('login')
    return redirect('dashboard')


@login_required(login_url='login')
def dashboard_view(request):
    wallet = request.user.wallet
    return render(request, 'wallet/dashboard.html', {'wallet': wallet})