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
    transactions = wallet.transactions.select_related('wallet').all()

    filter_type = request.GET.get('type', '')
    filter_date = request.GET.get('date', '')

    if filter_type:
        transactions = transactions.filter(transaction_type=filter_type)

    if filter_date:
        transactions = transactions.filter(created_at__date=filter_date)

    return render(request, 'wallet/transaction_list.html', {
        'transactions': transactions,
        'wallet': wallet,
        'filter_type': filter_type,
        'filter_date': filter_date,
        'selected_deposit': 'selected' if filter_type == 'deposit' else '',
        'selected_withdrawal': 'selected' if filter_type == 'withdrawal' else '',
        'selected_transfer': 'selected' if filter_type == 'transfer' else '',
    })


@login_required(login_url='login')
def transaction_detail_view(request, pk):
    transaction = get_object_or_404(
        Transaction.objects.select_related('wallet'),
        pk=pk,
        wallet=request.user.wallet
    )
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
def transaction_delete_view(request, pk):
    transaction = get_object_or_404(
        Transaction.objects.select_related('wallet'),
        pk=pk,
        wallet=request.user.wallet
    )

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transacción eliminada correctamente.')
        return redirect('transaction_list')

    return render(request, 'wallet/transaction_confirm_delete.html', {
        'transaction': transaction,
    })