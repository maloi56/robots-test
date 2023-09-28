from django.contrib import admin

from users.mixins import DisplayRoleMixin
from users.models import RegistrationQueries, User
from users.tasks import send_email_verification


@admin.register(User)
class UsersAdmin(DisplayRoleMixin, admin.ModelAdmin):
    list_display = ('email', 'display_role')


@admin.action(description="Подтвердить регистрацию")
def approve_registration(modeladmin, request, queryset):
    """
        Функция подтверждения регистрации пользователя. Создает пользователя, отправляет ему на почту данные для входа.
    """
    for obj in queryset:
        if not User.objects.filter(email=obj.email).exists():
            send_email_verification.delay(obj.pk)


@admin.register(RegistrationQueries)
class RegistrationRequestsAdmin(DisplayRoleMixin, admin.ModelAdmin):
    list_display = ['name', 'display_role', 'email', 'created']
    ordering = ['created']
    actions = [approve_registration]
    # readonly_fields = ['name', 'role', 'email', 'created']
