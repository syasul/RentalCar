from babel.numbers import format_currency

def currency(amount):
    return format_currency(amount, 'IDR', locale='id_ID')