from http import HTTPStatus

from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from orders.forms import OrderForm
from store.models import Product, Warehouse
from users.models import User


class StoreTestCase(TransactionTestCase):
    """
        Тестирование отправки запроса на регистрацию
    """

    def setUp(self) -> None:
        self.path = reverse('store:catalog')

    def test_catalog_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'R4C - Каталог')
        self.assertTemplateUsed(response, 'store/catalog.html')
        self.assertIsInstance(response.context_data['form'](), OrderForm)

    def test_products_view_queryset_ordering(self):
        response = self.client.get(reverse('store:catalog'))

        expected_order = ('-robot__quantity', 'robot__model', 'robot__version')
        queryset = response.context['products']
        self.assertEqual(queryset.query.order_by, expected_order)


class AddProductViewTest(TestCase):
    def setUp(self):
        self.password = 'testpassword'
        self.user = User.objects.create_user(email='testuser@mail.ru', password=self.password, role=User.ADMIN)
        self.warehouse_robot = Warehouse.objects.create(pk='1', model='r2', version='d2')
        self.warehouse_robot_empty = Warehouse.objects.create(pk='2', model='r2', version='d3', quantity=0)

    def test_add_product_view(self):

        """Тест доступа к странице"""

        path = reverse('store:add_product')
        response = self.client.get(path)
        self.assertRedirects(response, reverse('users:login') + '?next=' + path)

        temp_user = User.objects.create_user(email='testuser1@mail.ru', password=self.password, role=User.DIRECTOR)
        self.client.force_login(temp_user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'store/add_product.html')
        self.assertEqual(response.context_data['title'], 'R4C - Выставление на продажу')

    def test_add_product_view_form_submission(self):

        """Тест валидной формы создания продукта"""

        self.client.force_login(self.user)

        form_data = {
            'robot': f'{self.warehouse_robot.pk}',
            'description': 'ОПИСАНИЕ РОБОТА',
            'price': '12000',
        }

        response = self.client.post(reverse('store:add_product'), data=form_data)
        self.assertTrue(Product.objects.filter(robot=form_data['robot']).exists())
        self.assertRedirects(response, reverse('store:add_product'))

    def test_add_product_view_form_invalid_submission(self):

        """Тест невалидной формы создания продукта"""

        self.client.force_login(self.user)
        form_data = {
            'robot': '999',
            'description': 'ОПИСАНИЕ РОБОТА',
            'price': '12000',
        }
        response = self.client.post(reverse('store:add_product'), data=form_data)

        self.assertFalse(Product.objects.filter(robot=form_data['robot']).exists())
        self.assertEqual(response.status_code, 200)

    def test_add_product_view_form_invalid_robot_exists(self):

        """Тест попытки создания продукта который уже существует"""

        product = Product.objects.create(robot=self.warehouse_robot, price=1500)

        self.client.force_login(self.user)

        form_data = {
            'robot': f'{self.warehouse_robot.pk}',
            'description': 'ОПИСАНИЕ РОБОТА',
            'price': '12000',
        }

        response = self.client.post(reverse('store:add_product'), data=form_data)

        self.assertTrue('robot' in response.context['form'].errors)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/add_product.html')
