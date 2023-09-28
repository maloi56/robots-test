from http import HTTPStatus

from django.test import TransactionTestCase
from django.urls import reverse

from users.forms import RegistrationQueryForm, UserLoginForm
from users.models import RegistrationQueries, User
from users.tasks import send_email_verification


class UserRegistrationViewTestCase(TransactionTestCase):
    """
        Тестирование отправки запроса на регистрацию
    """

    def setUp(self) -> None:
        self.data = {'email': 'test@mail.ru',
                     'role': f'{User.TECH_SPEC}',
                     'name': 'test'}
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'R4C - Регистрация')
        self.assertEqual(response.template_name[0], 'users/registration.html')
        self.assertIsInstance(response.context_data['form'], RegistrationQueryForm)

    def test_user_registration_post_success(self):
        username = self.data['email']
        self.assertFalse(User.objects.filter(email=username).exists())
        self.assertFalse(RegistrationQueries.objects.filter(email=username).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(RegistrationQueries.objects.filter(email=username).exists())
        self.assertFalse(User.objects.filter(email=username).exists())

    def test_user_registration_post_error(self):
        RegistrationQueries.objects.create(email=self.data['email'])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Запрос на регистрацию с таким Email уже существует.')

        new_user = User.objects.create_user(email='vasya@mail.ru', password='testtest1', role=User.TECH_SPEC)

        RegistrationQueries.objects.create(email=new_user.email)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['form'].is_valid())


class LoginViewTestCase(TransactionTestCase):
    """
        Тестирование авторизации пользователей
    """

    def setUp(self) -> None:
        self.password = 'testtest1'
        self.user = User.objects.create_user(email='test@mail.ru',
                                             password=self.password,
                                             role=f'{User.TECH_SPEC}',
                                             name='test')
        self.path = reverse('users:login')

    def test_user_login_get_success(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'R4C - Авторизация')
        self.assertEqual(response.template_name[0], 'users/login.html')
        self.assertIsInstance(response.context_data['form'], UserLoginForm)

    def test_user_login_post_success(self):
        data = {'username': self.user.email,
                'password': self.password}

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_post_error(self):
        data = {'email': 'wrongemail@mail.ru',
                'password': 'wrongpass'}

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.context_data['form'].errors)


class ApproveRegistrationTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.query = RegistrationQueries.objects.create(email='dimatuchaa@gmail.com',
                                                        role=f'{User.TECH_SPEC}',
                                                        name='test')

    def test_approve_success(self):
        """
            Тестирование подтверждения регистрации
        """

        query = RegistrationQueries.objects.filter(email=self.query.email)
        self.assertTrue(query.exists())

        user = User.objects.filter(email=self.query.email)
        self.assertFalse(user.exists())

        send_email_verification(self.query.pk)

        self.assertTrue(user.exists())
        self.assertFalse(query.exists())
