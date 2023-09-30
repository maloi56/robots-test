from celery import shared_task
from celery_singleton import Singleton

from R4C.settings import LOGGER
from orders.models import Order


@shared_task(base=Singleton)
def send_order_notification_email(obj_pk):
    order = Order.objects.select_related('customer', 'product').get(pk=obj_pk)
    LOGGER.info(f'Task started: send_order_notification_email for {order}')
    if order.send_notification_email():
        order.delete()
        LOGGER.info(f'Task completed: send_order_notification_email for {order}')
