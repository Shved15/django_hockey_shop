from django.test import TestCase
from products.models import Product, ProductCategory


class ProductCategoryModelTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='Test Category', description='Test Description')

    def test_category_has_name(self):
        self.assertEqual(self.category.name, 'Test Category')

    def test_category_has_description(self):
        self.assertEqual(self.category.description, 'Test Description')

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), 'Test Category')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(name='Test Category', description='Test Description')
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=10.00,
                                              quantity=5, category=self.category)

    def test_product_has_name(self):
        self.assertEqual(self.product.name, 'Test Product')

    def test_product_has_description(self):
        self.assertEqual(self.product.description, 'Test Description')

    def test_product_has_price(self):
        self.assertEqual(self.product.price, 10.00)

    def test_product_has_quantity(self):
        self.assertEqual(self.product.quantity, 5)

    def test_product_has_category(self):
        self.assertEqual(self.product.category, self.category)

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), 'Product: Test Product || Category: Test Category')
