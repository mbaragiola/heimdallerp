from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo import models


class LocalityTestCase(APITestCase):
    """
    """
    fixtures = [
        'geo/tests/fixtures/users.json',
        'geo/tests/fixtures/geo.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:geo:locality-list')
        data = {
            'default_name': 'santa fe',
            'alternative_names': [
                {
                    'name': 'Holy Faith',
                    'language_code': 'en'
                },
                {
                    'name': 'Santa Fe',
                    'language_code': 'es'
                }
            ],
            'region': reverse(
                'api:geo:region-detail',
                args=[
                    models.Region.objects.get(default_name='Entre Ríos').pk
                ]
            )
        }  
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.Locality.objects.filter(default_name='Santa Fe').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Locality.objects.count(), 1)

    def test_correctness(self):
        obj = models.Locality.objects.get(
            default_name='santa fe'
        )
        self.assertEqual(obj.default_name, 'santa fe')
        self.assertEqual(
            obj.alternative_names.all()[0].name,
            'Holy Faith'
        )
        self.assertEqual(
            obj.alternative_names.all()[0].language_code,
            'en'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].language_code,
            'es'
        )
        self.assertEqual(
            obj.region,
            models.Region.objects.get(default_name='Entre Ríos')
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:geo:locality-detail',
            args=[models.Locality.objects.get(default_name='santa fe').pk]
        )
        data = {
            'default_name': 'Santa Fe',
            'alternative_names': [
                {
                    'id': (
                        models.AlternativeName.objects.get(
                            name='Holy Faith',
                            language_code='en'
                        ).pk
                    ),
                    'name': 'Santa Fe',
                    'language_code': 'en'
                },
                {
                    'id': (
                        models.AlternativeName.objects.get(
                            name='Santa Fe',
                            language_code='es'
                        ).pk
                    ),
                    'name': 'Santa Fe',
                    'language_code': 'es'
                },
                {
                    'name': 'Santa Fe',
                    'language_code': 'fr'
                }
            ],
            'region': reverse(
                'api:geo:region-detail',
                args=[models.Region.objects.get(default_name='Santa Fe').pk]
            )
        }  
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.Locality.objects.get(
            default_name='Santa Fe'
        )
        self.assertEqual(obj.default_name, 'Santa Fe')
        self.assertEqual(
            obj.alternative_names.all()[0].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[0].language_code,
            'en'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[1].language_code,
            'es'
        )
        self.assertEqual(
            obj.alternative_names.all()[2].name,
            'Santa Fe'
        )
        self.assertEqual(
            obj.alternative_names.all()[2].language_code,
            'fr'
        )
        self.assertEqual(
            obj.region,
            models.Region.objects.get(default_name='Santa Fe')
        )