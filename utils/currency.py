from babel.numbers import format_currency
from decimal import Decimal, InvalidOperation

def currency(amount):
    try:
        amount = Decimal(amount)
        return format_currency(amount, 'IDR', locale='id_ID')
    except (InvalidOperation, TypeError, ValueError):
        return "Invalid amount"
