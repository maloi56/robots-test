from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from management.excel_reports.reports import \
    generate_created_robots_per_period_report
from robots.models import Robot
from users.models import User


class ManagementTestCase(TransactionTestCase):
    """
        Тестирование отправки запроса на регистрацию
    """

    def setUp(self):
        self.password = 'testpassword'
        self.user_director = User.objects.create_user(email='director@mail.ru',
                                                      password=self.password,
                                                      role=User.DIRECTOR)
        self.non_director_user = User.objects.create_user(email='admin@mail.ru',
                                                          password=self.password,
                                                          role=User.ADMIN)

    def test_catalog_get(self):
        """Тест доступа к странице"""

        path = reverse('management:management')
        response = self.client.get(path)
        self.assertRedirects(response, reverse('users:login') + '?next=' + path)

        self.client.force_login(self.non_director_user)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user_director)
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'management/management.html')
        self.assertEqual(response.context_data['title'], 'R4C - management')


class GenerateCreatedRobotsPerPeriodReportTest(TransactionTestCase):
    def setUp(self):
        self.days_count = 7
        self.password = 'testpassword'
        self.user_director = User.objects.create_user(email='director@mail.ru',
                                                      password=self.password,
                                                      role=User.DIRECTOR)
        self.non_director_user = User.objects.create_user(email='admin@mail.ru',
                                                          password=self.password,
                                                          role=User.ADMIN)
        self.robot = Robot.objects.create(model='r2', version='d2')
        self.path = reverse('management:get_excel_report', args=[self.days_count])

    def test_get_excel_report(self):
        """Тест доступа к excel отчету"""

        response = self.client.get(self.path)
        self.assertRedirects(response, reverse('users:login') + '?next=' + self.path)

        self.client.force_login(self.non_director_user)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.user_director)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_excel_report_file_name(self):
        """
            Тест корректности названия файла
        """

        self.client.force_login(self.user_director)
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

        start_date = timezone.now() - timezone.timedelta(days=self.days_count)
        now = timezone.now().date().strftime('%d-%m')
        start_date_str = start_date.date().strftime('%d-%m')

        expected_filename = f'R4C_report_for_{start_date_str}:{now}_({self.days_count} days).xlsx'
        self.assertEqual(response['Content-Disposition'], f'attachment; filename={expected_filename}')

    def test_generate_created_robots_per_period_report(self):
        """
            Тест проверки что файл создается
        """
        start_date = timezone.now() - timezone.timedelta(days=self.days_count)
        workbook = generate_created_robots_per_period_report(self.days_count, start_date)

        self.assertIsNotNone(workbook)
        self.assertGreater(len(workbook.sheetnames), 0)
