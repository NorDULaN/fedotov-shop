from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Subscriber
from products.models import Product
from .forms import SubscriberForm
# Create your views here.

def HomeIndex(request):
    offers = Product.objects.filter(available=True)[:4]
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form_sub = form.cleaned_data
            try:
                new_sub = Subscriber.objects.get(email=form_sub['email'])
                form = SubscriberForm()
            except Subscriber.DoesNotExist:
                new_sub = Subscriber.objects.create(email=form_sub['email'])
                return HttpResponseRedirect('/thanks/')
    else:
        form = SubscriberForm()

    return render(request, 'landing/home/index.html', {
        'form': form,
        'offers': offers
    })
