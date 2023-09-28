import logging

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string

from users.managers import CustomUserManager

logger = logging.getLogger(__name__)


class User(AbstractUser):
    ADMIN = '0'
    DIRECTOR = '1'
    TECH_SPEC = '2'

    ROLE_CHOICES = ((None, 'Выберите должность'),
                    (DIRECTOR, 'Директор'),
                    (TECH_SPEC, 'Технический специалист'))

    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(verbose_name='логин', unique=True, blank=True, null=True)
    role = models.CharField(verbose_name='Роль', choices=ROLE_CHOICES, default=ADMIN, max_length=2,
                            help_text='Выбор роли пользователя: Директор/тех.специалист')
    name = models.CharField(verbose_name='Имя', max_length=32, null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class RegistrationQueries(models.Model):
    """
    Модель запросов директоров/технических специалистов на получение доступа к личному аккаунту.
    Администратор через админ панель подтверждает или отклоняет доступ.
    """

    email = models.EmailField(verbose_name='email', unique=True)
    name = models.CharField(verbose_name='Имя', max_length=32, null=True, blank=True)
    role = models.CharField(verbose_name='Роль', choices=User.ROLE_CHOICES, max_length=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "запрос на регистрацию"
        verbose_name_plural = "запросы на регистрацию"

    def __str__(self):
        return f'{self.email}: {self.created}'

    def send_registration_email(self, user_pk, password):
        """
        Функция для отправки данных для входа пользователю на почту.
        Удаляет запрос на создание аккаунт из БД.
        """
        try:
            logger.info(f'Task started: send_registration_email for {self.email}')
            user = User.objects.get(pk=user_pk)
            subject = 'Учетные данные для R4C'
            context = {'data': {'user': user, 'password': password}}
            html_message = render_to_string('registration_email.html', context)
            email = EmailMultiAlternatives(
                subject=subject,
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.email],
            )
            email.content_subtype = 'html'
            sent = email.send()
            if sent:
                self.delete()
            logger.info(f'Task completed: send_registration_email for {self.email}')
        except Exception as e:
            logger.error(f'Error in send_registration_email for {self.email}: {e}')
