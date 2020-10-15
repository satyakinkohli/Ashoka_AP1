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
def card_qty(product, cart):
	keys = cart.keys()
	for id in keys:
		if int(id) == product.id:
			return cart.get(id)
	return 0

