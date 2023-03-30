from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import CommonMixin
from products.models import Bag, Product, ProductCategory


# create controller-class for main page
class IndexView(CommonMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Hockey - Shop'


# create controller-class for catalog page
class ProductsListView(CommonMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Shop - Catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.kwargs.get('category_id')
        return context


class ProductDetailView(CommonMixin, DetailView):
    model = Product
    template_name = 'products/product.html'
    title = 'Shop - Product card'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context


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
