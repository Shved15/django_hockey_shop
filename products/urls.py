from django.urls import path

from products.views import ProductsListView, bag_add, bag_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('bags/add/<int:product_id>/', bag_add, name='bag_add'),
    path('bags/remove/<int:bag_id>/', bag_remove, name='bag_remove'),
]
