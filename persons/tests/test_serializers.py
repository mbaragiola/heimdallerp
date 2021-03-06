from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from persons import models
from rest_framework import status
from rest_framework.test import APITestCase


class PhysicalAddressTestCase(APITestCase):
    """
    """
    fixtures = [
        'persons/tests/fixtures/users.json',
        'persons/tests/fixtures/geo.json'
    ]

    def test_create(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:persons:physicaladdress-list')
        data = {
            'street_address': '9 de Julio 2454',
            'floor_number': '',
            'apartment_number': '',
            'locality': reverse(
                'api:geo:locality-detail',
                args=[
                    models.Locality.objects.get(default_name='Santa Fe').pk
                ]
            ),
            'postal_code': '3000'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CompanyTestCase(APITestCase):
    """
    """
    fixtures = [
        'persons/tests/fixtures/users.json',
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:persons:company-list')
        data = {
            'fantasy_name': 'IRONA',
            'slogan': 'tfw no slogan'
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Company.objects.filter(fantasy_name='IRONA').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Company.objects.count(), 1)

    def test_correctness(self):
        obj = models.Company.objects.get()
        self.assertEqual(obj.fantasy_name, 'IRONA')
        self.assertEqual(obj.slogan, 'tfw no slogan')
