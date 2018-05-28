from django.shortcuts import render, get_object_or_404, render_to_response
from .models import *
#from cart.forms import CartAddProductForm


# Страница с товарами
def ProductList(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'products/index.html', {
        'categories': categories,
    })

def show_category(request,hierarchy=None):

    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    categories = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Product, slug = category_slug[-1])
        #images = ProductImage.objects.filter(pk=instance ,is_active=True)
        return render(request, "products/productDetail.html", {
            'instance':instance,
            'categories': categories,
            })
    else:
        return render(request, 'products/productInCats.html', {
        'instance':instance,
        'categories': categories,
        })
