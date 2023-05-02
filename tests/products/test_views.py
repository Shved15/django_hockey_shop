from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_index_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Hockey - Shop')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Test Category', description='This is a test category')
        self.product = Product.objects.create(
            name='Test Product',
            description='This is a test product',
            price=10.0,
            quantity=5,
            image='test_image.jpg',
            category=self.category
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('products:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product.html')
        self.assertContains(response, self.product.name)

    def test_product_list_view_by_category(self):
        response = self.client.get(reverse('products:category', args=[self.category.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, self.product.name)

    def test_product_list_view_pagination(self):
        for i in range(10):
            Product.objects.create(
                name=f'Test Product {i}',
                description='This is a test product',
                price=10.0,
                quantity=5,
                image='test_image.jpg',
                category=self.category
            )

        response = self.client.get(reverse('products:paginator', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, 'Test Product 9')
        self.assertNotContains(response, 'Test Product 4')

