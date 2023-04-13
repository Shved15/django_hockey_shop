from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_index_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Hockey - Shop')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['goods_categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list_products(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:6]))

    def test_list_categories(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': 1})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def test_pagination(self):
        path1 = reverse('products:paginator', kwargs={'page': 1})
        path2 = reverse('products:paginator', kwargs={'page': 2})
        response1 = self.client.get(path1)
        response2 = self.client.get(path2)
        self._common_tests(response1)
        self._common_tests(response2)
        self.assertEqual(
            list(response1.context_data['object_list']),
            list(self.products[:6])
        )
        self.assertEqual(
            list(response2.context_data['object_list']),
            list(self.products[6:])
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Shop - Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
