from product.models import Currency
from django import template


def currency_price(price):
    currency = Currency.objects.get(title='hrn')
    currency_rate = currency.value
    final_price = price * currency_rate
    return round(final_price, 2)



def subtotal_currency(subtotal):
    currency = Currency.objects.get(title='hrn')
    currency_rate = currency.value
    final_price = subtotal * currency_rate
    return round(final_price, 2)


register = template.Library()
register.filter('currency_price', currency_price)
register.filter('subtotal_currency', subtotal_currency)