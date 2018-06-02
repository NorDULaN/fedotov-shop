from django.shortcuts import render
from products.models import Product, ProductImage
from django.utils import timezone
# Create your views here.

def HomeIndex(request):
    offers = Product.objects.filter(available=True, discount__gt=9)[:11]
    all_prod = Product.objects.filter(available=True,created__lte=timezone.now()).order_by('-created')[:11]
    #images = ProductImage.objects.filter(is_active=True, is_main=True, product__available=True)

    # if request.method == 'POST':
    #     form = SubscriberForm(request.POST)
    #     if form.is_valid():
    #         form_sub = form.cleaned_data
    #         try:
    #             new_sub = Subscriber.objects.get(email=form_sub['email'])
    #             form = SubscriberForm()
    #
    #         except Subscriber.DoesNotExist:
    #             new_sub = Subscriber.objects.create(email=form_sub['email'])
    #
    # else:
    #     form = SubscriberForm()
    return render(request, 'landing/index.html', {
        'offers': offers,
        'all_prod': all_prod,
    })


def InfoIndex(request):
    return render(request, 'landing/info.html', locals())


def OrderingIndex(request):
    return render(request, 'landing/zakaz.html', locals())


def DeliveryIndex(request):
    return render(request, 'landing/dostavka.html', locals())        
