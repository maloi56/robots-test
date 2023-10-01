from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from robots.models import Robot
from store.models import Warehouse
from users.models import User


class UsersApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(email='techspec@mail.ru', password='testtesttest1', role=User.TECH_SPEC)

    def setUp(self) -> None:
        self.user = User.objects.get(email='techspec@mail.ru')
        self.token = self.user.auth_token.key
        self.headers = {'Authorization': 'Token ' + self.token}
        self.url = reverse('robots-list')

    def test_post_robot(self):
        # without auth
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        # not allowed get
        response = self.client.get(self.url, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

        # empty body
        response = self.client.post(self.url, headers=self.headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # error body
        data = {
            'not_valid_field': 'asdsadsad'
        }
        response = self.client.post(self.url, headers=self.headers, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # successful post
        r2_robot = Robot.objects.filter(model='r2').exists()
        self.assertFalse(r2_robot)
        data = {
            'model': 'r2',
            'version': 'd2',
            'serial': 1
        }
        response = self.client.post(self.url, headers=self.headers, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        r2_robot = Robot.objects.filter(model='r2').exists()
        self.assertTrue(r2_robot)

        # successful post many
        robots = Robot.objects.filter(model__in=['r3', 'd3']).count()
        self.assertEqual(robots, 0)
        data = [
            {
                'model': 'r3',
                'version': 'd3',
                'serial': 1
            },
            {
                'model': 'r4',
                'version': 'd4',
                'serial': 1
            },
        ]
        response = self.client.post(self.url, headers=self.headers, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        robots = Robot.objects.filter(model__in=['r3', 'r4']).count()
        self.assertEqual(robots, 2)

    def test_robots_signals(self):
        # check of creating warehouse instance
        warehouse = Warehouse.objects.all().count()
        self.assertEqual(warehouse, 0)

        data = {
            'model': 'r2',
            'version': 'd2',
            'serial': 1
        }
        response = self.client.post(self.url, headers=self.headers, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        warehouse = Warehouse.objects.get(model='r2', version='d2')
        self.assertEqual(warehouse.quantity, 1)

        # check of updating warehouse instance
        response = self.client.post(self.url, headers=self.headers, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        warehouse = Warehouse.objects.get(model='r2', version='d2')
        self.assertEqual(warehouse.quantity, 2)
