from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import CommonMixin
from products.models import Bag, Favorites, Product, ProductCategory


class IndexView(CommonMixin, TemplateView):
    """Index view that displays the homepage of the website."""
    template_name = 'products/index.html'
    title = 'Hockey - Shop'


class ProductsListView(CommonMixin, ListView):
    """List view that displays the products available in the shop."""
    model = Product
    template_name = 'products/products.html'
    paginate_by = 6
    title = 'Shop - Catalog'

    def get_queryset(self):
        """Override of the `get_queryset` method to filter products by category ID."""
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id).order_by('name') \
            if category_id else queryset.order_by('name')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Override of the `get_context_data` method to add category data to the context."""
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.kwargs.get('category_id')
        return context


class ProductSearchView(CommonMixin, ListView):
    """View for searching products by name or description."""
    model = Product
    template_name = 'products/search_products_by_name.html'
    paginate_by = 6
    title = 'Shop - Catalog'

    def get_queryset(self):
        """Overrides the get_queryset method to filter the Product model queryset
         based on a search query parameter."""
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query is not None and query.strip():
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            # if the query is not set, then return an empty QuerySet
            queryset = queryset.none()
        print(queryset)
        return queryset.order_by('name')


class ProductDetailView(CommonMixin, DetailView):
    """View for displaying a single product."""
    model = Product
    template_name = 'products/product.html'
    title = 'Shop - Product card'

    def get_context_data(self, **kwargs):
        """Overrides the get_context_data method to add additional context variables
         for rendering the product template."""
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        return context


@login_required
def bag_add(request, product_id):
    Bag.create_or_update(product_id=product_id, user=request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bag_remove(request, bag_id):
    bag = Bag.objects.get(id=bag_id)
    bag.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class FavListView(CommonMixin, ListView):
    model = Favorites
    template_name = 'products/favorites.html'
    title = 'Favorite'
    paginate_by = 6
    queryset = Favorites.objects.all()

    def get_queryset(self):
        """Override the queryset to show the user's favorites only."""
        queryset = super(FavListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id, user=self.request.user) if category_id else queryset.filter(
            user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add categories and category_id to the context."""
        context = super(FavListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.kwargs.get('category_id')
        return context


@login_required
def fav_add(request, product_id):
    product = Product.objects.get(id=product_id)
    favorites = Favorites.objects.filter(user=request.user, product=product)

    if not favorites.exists():
        Favorites.objects.create(user=request.user, product=product)
    else:
        favorite = favorites.first()
        favorite.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def fav_remove(request, favorite_id):
    favorite = Favorites.objects.get(id=favorite_id)
    favorite.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
