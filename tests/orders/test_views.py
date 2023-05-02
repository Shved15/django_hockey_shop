from django.test import Client, TestCase
from django.urls import reverse

from orders.models import Order
from users.models import User


class OrderSuccessTemplateViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('orders:order_success')

    def test_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/successfully.html')


class OrderCanceledTemplateViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('orders:order_cancel')
        self.response = self.client.get(self.url)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'orders/canceled.html')


class OrderListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create test user
        test_user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        test_user.save()

        # create test orders for the test user
        Order.objects.create(
            first_name='Max',
            last_name='Vax',
            email='maxvax@example.com',
            address='123 Main St',
            creator=test_user
        )
        Order.objects.create(
            first_name='Xam',
            last_name='Xav',
            email='xamxav@example.com',
            address='456 Oak St',
            creator=test_user
        )

    def test_order_list_view(self):
        # login as the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

        # make a GET request to the order list view
        response = self.client.get(reverse('orders:orders_list'))

        # verify that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # verify that the orders displayed are only those created by the test user
        orders = response.context['object_list']
        for order in orders:
            self.assertEqual(order.creator.username, 'testuser')
