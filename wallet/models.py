from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('CLP', 'Chilean Peso'),
    ]
    
    user = models.OneToOneField( #Un usuario tiene exactamente una wallet, no más
        User,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField( #Dinero nunca se guarda en FloatField — los floats tienen errores de precisión binaria que en fintech son inaceptables
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    currency = models.CharField( #Limita los valores válidos a nivel de formulario y admin
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    created_at = models.DateTimeField(auto_now_add=True) #Se asigna una sola vez al crear el registro, nunca se modifica

    def __str__(self):
        return f"{self.user.username} — {self.currency} {self.balance}"


class Transaction(models.Model):
    
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    wallet = models.ForeignKey( #Una wallet puede tener muchas transacciones
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.DecimalField( #Se utiliza DecimalField para evitar errores en redondeos.
        max_digits=12,
        decimal_places=2
    )
    transaction_type = models.CharField( #Controla el vocabulario del dominio: solo 3 valores válidos
        max_length=10,
        choices=TRANSACTION_TYPES
    )
    description = models.CharField( #Es opcional — una transferencia puede no necesitar nota
        max_length=255,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True) #La fecha de una transacción es inmutable, como en la vida real

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} — {self.amount} ({self.wallet.user.username})"