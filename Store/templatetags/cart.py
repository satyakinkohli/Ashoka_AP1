from django import template

register = template.Library()

@register.filter(name='is_in_cart')

def is_in_cart(product):
	#keys = cart.keys()
	#for id in keys:
		#if id == product.id:
			#return True
	#return False;
	print(product)
	return True;


