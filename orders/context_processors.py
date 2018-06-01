from .models import ProductInCart


def user_cart_info(request):
	session_key = request.session.session_key
    if not session_key:
        #workaround for newer Django versions
        request.session["session_key"] = 123
        #re-apply value
        request.session.cycle_key()
	items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
	items_in_cart_price = 0
	items_in_cart_count = 0
	for item in items_in_cart:
		items_in_cart_price += float(item.total_price)
		items_in_cart_count += item.count
	#items_in_cart_count = items_in_cart.count
	return locals()
