from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, TransactionForm
from .models import Wallet, Transaction


# ─── Autenticación ────────────────────────────────────────────────────────────

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
    recent_transactions = wallet.transactions.all()[:5]
    return render(request, 'wallet/dashboard.html', {
        'wallet': wallet,
        'recent_transactions': recent_transactions,
    })


# ─── Transacciones ────────────────────────────────────────────────────────────

@login_required(login_url='login')
def transaction_list_view(request):
    wallet = request.user.wallet
    transactions = wallet.transactions.all()
    return render(request, 'wallet/transaction_list.html', {
        'transactions': transactions,
        'wallet': wallet,
    })


@login_required(login_url='login')
def transaction_detail_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, wallet=request.user.wallet)
    return render(request, 'wallet/transaction_detail.html', {
        'transaction': transaction,
    })


@login_required(login_url='login')
def transaction_create_view(request):
    wallet = request.user.wallet

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = wallet
            transaction.save()
            messages.success(request, 'Transacción registrada correctamente.')
            return redirect('transaction_list')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = TransactionForm()

    return render(request, 'wallet/transaction_form.html', {
        'form': form,
        'action': 'Crear',
    })


@login_required(login_url='login')
def transaction_edit_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, wallet=request.user.wallet)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción actualizada correctamente.')
            return redirect('transaction_detail', pk=transaction.pk)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'wallet/transaction_form.html', {
        'form': form,
        'action': 'Editar',
        'transaction': transaction,
    })


@login_required(login_url='login')
def transaction_delete_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, wallet=request.user.wallet)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transacción eliminada correctamente.')
        return redirect('transaction_list')

    return render(request, 'wallet/transaction_confirm_delete.html', {
        'transaction': transaction,
    })