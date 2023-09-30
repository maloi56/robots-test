from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string

from R4C.settings import LOGGER
from customers.models import Customer
from store.models import Warehouse


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(to=Warehouse, related_name='orders', on_delete=models.CASCADE,
                                help_text='Связь с роботом на складе')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.pk}. {self.customer}'

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
        unique_together = ("customer", "product")

    def send_notification_email(self):
        try:
            subject = 'Робот снова в наличии!'
            context = {'product': self.product}
            html_message = render_to_string('order_notification_email.html', context)
            email = EmailMultiAlternatives(
                subject=subject,
                body=html_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.customer.email],
            )
            email.content_subtype = 'html'
            sent = email.send()
            if sent:
                return True
        except Exception as e:
            LOGGER.error(f'Error in send_registration_email for {self}: {e}')
            return False
