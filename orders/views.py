from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import *
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from .forms import *
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail


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

    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
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
    session_key = request.session.session_key
    checkout = ProductInCart.objects.filter(session_key=session_key, is_active=True)
    checkout_count = checkout.count()
    checkout_endprice = 0
    for item in checkout:
        checkout_endprice += float(item.total_price)
    if checkout_count < 1:
        return render(request, 'orders/orderCheckout.html', locals())
        
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form_order = form.cleaned_data
            status = OrderStatus.objects.get(pk=1)
            new_order = Order.objects.create(customer_name=form_order['customer_name'],
            customer_email=form_order['customer_email'],customer_phone=form_order['customer_phone'],
            customer_region=form_order['customer_region'],customer_city=form_order['customer_city'],
            customer_index=form_order['customer_index'],customer_comment=form_order['customer_comment'],
            status=status,total_price=checkout_endprice)

            for prod_in_ord in checkout:
                ord = ProductInOrder.objects.create(order=new_order, product=prod_in_ord.product)
                ord.count=prod_in_ord.count
                ord.save(force_update=True)
                ProductInCart.objects.filter(session_key=session_key, pk=prod_in_ord.id).delete()

            new_order.save(force_update=True)
            # Отправка Email
            prod_in_ord = ProductInOrder.objects.filter(order=new_order, is_active=True)
            msg_plain = render_to_string('orders/email.txt', {'new_order': new_order, 'prod_in_ord': prod_in_ord})
            msg_html = render_to_string('orders/email.html', {'new_order': new_order, 'prod_in_ord': prod_in_ord})
            subject = 'Онлайн-магазин - заказ: #{}'.format(new_order.id)
            send_mail(
                subject,
                msg_plain,
                'yechezlaip@gmail.com',
                [new_order.customer_email],
                html_message=msg_html,
            )
            return render(request, 'orders/orderEnd.html', {'new_order': new_order})
    else:
        form = OrderForm()
    return render(request, 'orders/orderCheckoutForm.html', locals())

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
    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
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

    items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
    items_in_cart_price = 0
    items_in_cart_count = 0
    for item in items_in_cart:
        items_in_cart_price += float(item.total_price)
        items_in_cart_count += item.count

    #items_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["items_in_cart_price"] = items_in_cart_price
    return_dict["items_in_cart_count"] = items_in_cart_count
    return JsonResponse(return_dict)
