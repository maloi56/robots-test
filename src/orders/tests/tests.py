from unittest import TestCase

from django.test import TestCase
from django.urls import reverse

from customers.models import Customer
from orders.models import Order
from store.models import Warehouse


class CreateOrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Warehouse.objects.create(pk=1, model='r2', version='d2', quantity=0)
        Customer.objects.create(email='dimatuchaa@gmail.com')

    def setUp(self) -> None:
        self.path = reverse('orders:create_order')

    def test_create_order_view_valid_form(self):
        """
            Успешное создание заявки
        """

        form_data = {
            'email': 'test@example.com',
            'product': '1',
        }
        response = self.client.post(self.path, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_view_invalid_form(self):
        """
            Создание заявки с ошибкой
        """
        form_data = {
            'email': 'invalid_email',
            'product': 1,
        }
        response = self.client.post(self.path, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)

    def test_send_notification_email(self):
        """
            Отправка письма
        """
        product = Warehouse.objects.get(pk=1)
        customer = Customer.objects.get(email='dimatuchaa@gmail.com')
        order = Order.objects.create(customer=customer, product=product)
        result = order.send_notification_email()

        self.assertTrue(result)
