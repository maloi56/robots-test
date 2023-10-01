from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from orders.tasks import send_order_notification_email
from robots.models import Robot
from store.models import Warehouse


@receiver(post_save, sender=Robot)
def create_robot(sender, instance=None, created=False, **kwargs):
    if created:
        warehouse, created = Warehouse.objects.get_or_create(model=instance.model, version=instance.version)
        if not created:
            warehouse.quantity += 1
            warehouse.save()

            orders = Order.objects.filter(product=warehouse)
            for order in orders:
                send_order_notification_email.delay(order.pk)
