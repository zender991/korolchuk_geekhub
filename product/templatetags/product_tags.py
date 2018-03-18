from product.models import Currency
from django import template


def currency_price(price):
    currency = Currency.objects.get(title='hrn')
    currency_rate = currency.value
    return price * currency_rate



def subtotal_currency(subtotal):
    currency = Currency.objects.get(title='hrn')
    currency_rate = currency.value
    return subtotal * currency_rate


register = template.Library()
register.filter('currency_price', currency_price)
register.filter('subtotal_currency', subtotal_currency)