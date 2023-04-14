from http import HTTPStatus

from django.test import Client, TestCase
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


class ProductSearchViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('products:search_results')
        self.category = ProductCategory.objects.create(name='Default')
        self.product1 = Product.objects.create(name='Test1', description='Description1',
                                               price=10.0, quantity=5, category=self.category)
        self.product2 = Product.objects.create(name='Test2', description='Description2',
                                               price=15.0, quantity=10, category=self.category)
        self.product3 = Product.objects.create(name='Test3', description='Description3',
                                               price=20.0, quantity=15, category=self.category)

    def test_search_products_by_name(self):
        response = self.client.get(self.url, {'q': 'Test1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertNotContains(response, self.product2.name)
        self.assertNotContains(response, self.product3.name)
        print(response.content.decode())

    def test_search_products_by_description(self):
        response = self.client.get(self.url, {'q': 'Description2'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        self.assertNotContains(response, self.product3.name)

    def test_empty_query(self):
        response = self.client.get(self.url, {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], Product.objects.none())

    def test_no_match_query(self):
        response = self.client.get(self.url, {'q': 'No match'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'There are no matches for your "{response.request.get("q")}" search.')
