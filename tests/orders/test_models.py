from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Order


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.order = Order.objects.create(
            first_name='TestName',
            last_name='TestSurname',
            email='testmail@example.com',
            address='123 Main St',
            bag_history={'item1': 1, 'item2': 2},
            state=Order.PAID,
            creator=self.user,
        )

    def test_order_creation(self):
        self.assertEqual(str(self.order), 'Order №1. TestName TestSurname')
        self.assertEqual(self.order.first_name, 'TestName')
        self.assertEqual(self.order.last_name, 'TestSurname')
        self.assertEqual(self.order.email, 'testmail@example.com')
        self.assertEqual(self.order.address, '123 Main St')
        self.assertEqual(self.order.bag_history, {'item1': 1, 'item2': 2})
        self.assertEqual(self.order.state, Order.PAID)
        self.assertEqual(self.order.creator, self.user)
        self.assertIsNotNone(self.order.created)

    def test_order_states(self):
        self.assertEqual(Order.CREATED, 0)
        self.assertEqual(Order.PAID, 1)
        self.assertEqual(Order.ON_WAY, 2)
        self.assertEqual(Order.DELIVERED, 3)

