from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Transacciones
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('transactions/new/', views.transaction_create_view, name='transaction_create'),
    path('transactions/<int:pk>/', views.transaction_detail_view, name='transaction_detail'),
    path('transactions/<int:pk>/delete/', views.transaction_delete_view, name='transaction_delete'),
    # transaction_edit eliminado intencionalmente — las transacciones son inmutables
]