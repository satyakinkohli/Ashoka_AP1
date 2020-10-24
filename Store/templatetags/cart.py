from django import template
from django.views import View

from Store.models import Order
from Store.models.wishlist import Wishlist

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


@register.filter(name='number_interested')
def number_interested(product_id):
    serial = list(Wishlist.get_wishlist_by_productid(product_id))
    return len(serial)


@register.filter(name='ratings')
def ratings(product_id):
    serial = Order.get_orders_by_orderid(product_id)
    total_ratings = len(serial)

    if total_ratings == 0:
        total_ratings = 1
    else:
        pass

    opinion = 0
    for item in serial:
        opinion += item.rating

    rated = round((opinion / total_ratings), 2)
    if rated == 0:
        rated = "-"
    else:
        pass

    return rated
