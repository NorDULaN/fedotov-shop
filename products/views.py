from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product
#from cart.forms import CartAddProductForm


# Страница с товарами
def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

# Страница товара
def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    #cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html',
                             {'product': product,
                              #'cart_product_form': cart_product_form}
                              })

def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Product, slug = category_slug[-1])
        return render(request, "products/productDetail.html", {'instance':instance})
    else:
        return render(request, 'products/products.html', {'instance':instance})
