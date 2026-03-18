from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction


def recalculate_balance(wallet):
    from django.db.models import Sum, Case, When, DecimalField

    result = wallet.transactions.aggregate(
        total=Sum(
            Case(
                When(transaction_type='deposit', then='amount'),
                When(transaction_type='withdrawal', then=-1 * 1),
                When(transaction_type='transfer', then=-1 * 1),
                default=0,
                output_field=DecimalField()
            )
        )
    )

    # Recalcula sumando depósitos y restando retiros y transferencias
    from decimal import Decimal
    deposits = wallet.transactions.filter(
        transaction_type='deposit'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    outflows = wallet.transactions.filter(
        transaction_type__in=['withdrawal', 'transfer']
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    wallet.balance = deposits - outflows
    wallet.save()


@receiver(post_save, sender=Transaction)
def update_balance_on_save(sender, instance, **kwargs):
    recalculate_balance(instance.wallet)


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    recalculate_balance(instance.wallet)
    