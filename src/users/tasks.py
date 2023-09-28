from celery import shared_task
from celery_singleton import Singleton

from users.models import RegistrationQueries, User


@shared_task(base=Singleton)
def send_email_verification(obj_pk):
    reg_query = RegistrationQueries.objects.get(pk=obj_pk)
    password = User.objects.make_random_password(12)
    user = User.objects.create_user(email=reg_query.email, password=password, role=reg_query.role)
    reg_query.send_registration_email(user.pk, password)
