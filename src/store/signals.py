from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from robots.models import Robot
from store.models import Warehouse


@receiver(post_save, sender=Robot)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        warehouse, created = Warehouse.objects.get_or_create(model=instance.model, version=instance.version)
        if not created:
            warehouse.quantity += 1
            warehouse.save()
