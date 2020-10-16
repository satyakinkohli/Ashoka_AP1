from django import template
from django.views import View

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='cart_qty')
def cart_qty(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0


@register.filter(name='item_total')
def item_total(product, cart):
    return product.price * cart_qty(product, cart)


@register.filter(name='cart_total')
def cart_total(products, cart):
    total = 0
    for product in products:
        total += item_total(product, cart)

    return total


@register.filter(name='multiply')
def multiply(number0, number1):
    return number0 * number1


@register.filter(name='total_products')
def total_products(cart):
    sum = 0
    if cart:
        for x in cart.values():
            sum += int(x)

    return sum
