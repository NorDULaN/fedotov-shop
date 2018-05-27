from django.http import JsonResponse
from .models import ProductInCart

def ordersAdd(request):
    return_dict = dict()

    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    item_id = data.get("item_id")
    item_quantity = data.get("item_quantity")

    new_product, created = ProductInCart.objects.get_or_create(session_key=session_key, product_id=item_id, defaults={"count":item_quantity})
    if not created:
        new_product.count += int(item_quantity)
        new_product.save(force_update=True)

    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["items_in_cart"] = items_in_cart
    return JsonResponse(return_dict)
