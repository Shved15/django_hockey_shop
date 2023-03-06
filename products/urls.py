from django.urls import path

from products.views import products, bag_add, bag_remove


app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('bags/add/<int:product_id>/', bag_add, name='bag_add'),
    path('bags/remove/<int:bag_id>/', bag_remove, name='bag_remove'),
]
