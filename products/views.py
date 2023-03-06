from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from products.models import ProductCategory, Product, Bag


# controller-function for main page
def index(request):
    context = {
        'title': "Hockey Shop",
    }
    return render(request, 'products/index.html', context)


# controller-function for catalog page
def products(request):
    context = {
        'title': 'Shop - Catalog',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'products/products.html', context)


# controller-functions for add and remove in bag
@login_required
def bag_add(request, product_id):
    product = Product.objects.get(id=product_id)
    bags = Bag.objects.filter(user=request.user, product=product)

    if not bags.exists():
        Bag.objects.create(user=request.user, product=product, quantity=1)
    else:
        bag = bags.first()
        bag.quantity += 1
        bag.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bag_remove(request, bag_id):
    bag = Bag.objects.get(id=bag_id)
    bag.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
