from django.urls import path

from products.views import ProductsListView, bag_add, bag_remove, ProductDetailView, fav_add, fav_remove, FavListView

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('product/<pk>/', ProductDetailView.as_view(), name='product'),

    path('bags/add/<int:product_id>/', bag_add, name='bag_add'),
    path('bags/remove/<int:bag_id>/', bag_remove, name='bag_remove'),

    path('fav/category/<int:category_id>/', FavListView.as_view(), name='fav_category'),
    path('fav/page/<int:page>/', FavListView.as_view(), name='fav_paginator'),
    path('fav/add/<int:product_id>/', fav_add, name='fav_add'),
    path('fav/remove/<int:favorite_id>/', fav_remove, name='fav_remove'),
]
