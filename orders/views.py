from django.http import JsonResponse
from .models import ProductInCart
from django.shortcuts import render, get_object_or_404, render_to_response, redirect


def ordersAdd(request):
    return_dict = dict()

    session_key = request.session.session_key
    data = request.POST
    item_id = data.get("item_id")
    item_quantity = data.get("item_quantity")
    if int(item_quantity) < 1:
        return JsonResponse(status=400)
    new_product, created = ProductInCart.objects.get_or_create(session_key=session_key, product_id=item_id, defaults={"count":item_quantity})
    if not created:
        new_product.count += int(item_quantity)
        new_product.save(force_update=True)

    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    items_in_cart_price = 0
    items_in_cart_count = 0
    for item in items_in_cart:
        items_in_cart_price += float(item.total_price)
        items_in_cart_count += item.count

    #items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["items_in_cart_price"] = items_in_cart_price
    return_dict["items_in_cart_count"] = items_in_cart_count
    return JsonResponse(return_dict)

def ordersCheckout(request):
    session_key = request.session.session_key
    checkout = ProductInCart.objects.filter(session_key=session_key, is_active=True)
    checkout_count = checkout.count()
    checkout_endprice = 0
    for item in checkout:
        checkout_endprice += float(item.total_price)
    return render(request, 'orders/orderCheckout.html', locals())

def ordersCheckoutForm(request):

    return JsonResponse(status=400)

def ordersCheckoutContinue(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    id = data.get("id")
    count = data.get("count")
    if int(count) < 1:
        return JsonResponse(status=400)
    new_product, created = ProductInCart.objects.get_or_create(session_key=session_key, product_id=id, defaults={"count":count})
    if not created:
        new_product.count = int(count)
        new_product.save(force_update=True)
    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    items_in_cart_price = 0
    items_in_cart_count = 0
    for item in items_in_cart:
        items_in_cart_price += float(item.total_price)
        items_in_cart_count += item.count

    #items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["items_in_cart_price"] = items_in_cart_price
    return_dict["items_in_cart_count"] = items_in_cart_count
    return JsonResponse(return_dict)

def ordersCheckoutRemove(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    id = data.get("id")
    count = data.get("count")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInCart.objects.filter(session_key=session_key, product_id=id).delete() #update(is_active=False)
    else:
        if int(count) < 1:
            return JsonResponse(status=400)
        new_product, created = ProductInCart.objects.get_or_create(session_key=session_key, product_id=id, defaults={"count":count})
        if not created:
            new_product.count = int(count)
            new_product.save(force_update=True)

    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    items_in_cart_price = 0
    items_in_cart_count = 0
    for item in items_in_cart:
        items_in_cart_price += float(item.total_price)
        items_in_cart_count += item.count

    #items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["items_in_cart_price"] = items_in_cart_price
    return_dict["items_in_cart_count"] = items_in_cart_count
    return JsonResponse(return_dict)
