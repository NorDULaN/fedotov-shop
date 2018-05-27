from .models import ProductInCart


def user_cart_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return locals()
