from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView

from common.view import RoleMixin, TitleMixin
from management.excel_reports.reports import \
    generate_created_robots_per_period_report
from robots.models import Robot
from users.models import User


class ManagementView(RoleMixin, TitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'management/management.html'
    login_url = reverse_lazy('users:login')
    title = 'R4C - management'
    model = Robot
    context_object_name = 'result'
    role = User.DIRECTOR


@login_required()
def get_excel_report(request, days_count):
    """
        Получение отчета произведенных роботов за :param days_count: дней
    """

    if request.user.role != User.DIRECTOR:
        raise PermissionDenied

    start_date = timezone.now() - timezone.timedelta(days=days_count)
    workbook = generate_created_robots_per_period_report(days_count, start_date)

    now = timezone.now().date().strftime('%d-%m')
    start_date_str = start_date.date().strftime('%d-%m')
    filename = f'R4C_report_for_{start_date_str}:{now}_({days_count} days).xlsx'

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    workbook.save(response)

    return response
