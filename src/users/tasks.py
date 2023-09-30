from celery import shared_task
from celery_singleton import Singleton

from R4C.settings import LOGGER
from users.models import RegistrationQueries, User


@shared_task(base=Singleton)
def send_email_verification(obj_pk):
    reg_query = RegistrationQueries.objects.get(pk=obj_pk)
    LOGGER.info(f'Task started: send_registration_email for {reg_query.email}')
    password = User.objects.make_random_password(12)
    user = User.objects.create_user(email=reg_query.email, password=password, role=reg_query.role, name=reg_query.name)
    res = reg_query.send_registration_email(user.pk, password)
    if res:
        reg_query.delete()
    LOGGER.info(f'Task completed: send_registration_email for {reg_query.email}')
