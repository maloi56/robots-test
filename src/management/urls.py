from django.urls import path

from management.views import ManagementView, get_excel_report

app_name = 'management'

urlpatterns = [
    path('', ManagementView.as_view(), name='management'),
    path('get_excel_report/<int:days_count>', get_excel_report, name='get_excel_report'),
]
