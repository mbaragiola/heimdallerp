from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contact.models import Contact
from geo.models import Locality, Country
from persons.models import Company
from invoice import models


class FiscalPositionTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice/tests/fixtures/users.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice:fiscalposition-list')
        data = {
            'name': 'Do Easy',
            'code': ''
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.FiscalPosition.objects.get(name='Do Easy').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.FiscalPosition.objects.count(), 1)

    def test_correctness(self):
        obj = models.FiscalPosition.objects.get(name='Do Easy')
        self.assertEqual(obj.name, 'Do Easy')
        self.assertEqual(obj.code, '')


class VATTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice/tests/fixtures/users.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice:vat-list')
        data = {
            'name': '10',
            'tax': 0.10,
            'code': '',
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.VAT.objects.get().delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.VAT.objects.count(), 1)

    def test_correctness(self):
        obj = models.VAT.objects.get(name='10')
        self.assertEqual(obj.name, '10')
        self.assertEqual(obj.tax, Decimal('0.10'))
        self.assertEqual(obj.code, '')

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:invoice:vat-detail',
            args=[models.VAT.objects.get(name='10').pk]
        )
        data = {
            'name': '-10',
            'tax': -0.10,
            'code': '',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        obj = models.VAT.objects.get(name='10')
        self.assertEqual(obj.name, '10')
        self.assertEqual(obj.tax, Decimal('0.10'))
        self.assertEqual(obj.code, '')

        data = {
            'name': '110',
            'tax': 1.10,
            'code': ''
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
 
        obj = models.VAT.objects.get(name='10')
        self.assertEqual(obj.name, '10')
        self.assertEqual(obj.tax, Decimal('0.10'))
        self.assertEqual(obj.code, '')

        data = {
            'name': '20',
            'tax': 0.20,
            'code': ''
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.VAT.objects.get(name='20')
        self.assertEqual(obj.name, '20')
        self.assertEqual(obj.tax, Decimal('0.20'))
        self.assertEqual(obj.code, '')


class CompanyInvoiceTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice/tests/fixtures/users.json',
        'invoice/tests/fixtures/geo.json',
        'invoice/tests/fixtures/invoicing.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice:companyinvoice-list')
        data = {
            'persons_company': {
                'fantasy_name': 'IRONA',
                'legal_name': 'Baragiola-Zanitti SH',
                'slogan': 'tfw no slogan',
                'initiated_activities': '2016-01-01'
            },
            'fiscal_position': (
                reverse('api:invoice:fiscalposition-detail', args=[1])
            ),
            'fiscal_address': {
                'street_address': '9 de Julio 2454',
                'floor_number': '',
                'apartment_number': '',
                'locality': reverse('api:geo:locality-detail', args=[1]),
                'postal_code': '3000'
            },
            'default_invoice_debit_account': '',
            'default_invoice_credit_account': ''
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.CompanyInvoice.objects.filter(
            persons_company__fantasy_name='ANORI'
        ).delete()
        Company.objects.filter(fantasy_name='ANORI').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.CompanyInvoice.objects.count(), 1)

    def test_correctness(self):
        obj = models.CompanyInvoice.objects.get(
            persons_company__fantasy_name='IRONA'
        )
        self.assertEqual(
            obj.persons_company.fantasy_name,
            'IRONA'
        )
        self.assertEqual(
            obj.persons_company.legal_name,
            'Baragiola-Zanitti SH'
        )
        self.assertEqual(
            obj.persons_company.slogan,
            'tfw no slogan'
        )
        self.assertEqual(
            obj.persons_company.initiated_activities,
            date(2016, 1, 1)
        )
        self.assertEqual(
            obj.fiscal_position,
            models.FiscalPosition.objects.get(name='Do Easy')
        )
        self.assertEqual(
            obj.fiscal_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.fiscal_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.fiscal_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.fiscal_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.fiscal_address.postal_code,
            '3000'
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:invoice:companyinvoice-detail',
            args=[
                models.CompanyInvoice.objects.get(
                    persons_company__fantasy_name='IRONA'
                ).pk
            ]
        )
        data = {
            'persons_company': {
                'fantasy_name': 'ANORI',
                'legal_name': 'Zanitti-Baragiola SH',
                'slogan': 'when face the slogan no',
                'initiated_activities': '2015-02-03'
            },
            'fiscal_position': (
                reverse('api:invoice:fiscalposition-detail', args=[2])
            ),
            'fiscal_address': {
                'street_address': 'San Martín 1100',
                'floor_number': '1',
                'apartment_number': '2',
                'locality': reverse('api:geo:locality-detail', args=[2]),
                'postal_code': '2000'
            },
            'default_invoice_debit_account': '',
            'default_invoice_credit_account': ''
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.CompanyInvoice.objects.get(
            persons_company__fantasy_name='ANORI'
        )
        self.assertEqual(
            obj.persons_company.fantasy_name,
            'ANORI'
        )
        self.assertEqual(
            obj.persons_company.legal_name,
            'Zanitti-Baragiola SH'
        )
        self.assertEqual(
            obj.persons_company.slogan,
            'when face the slogan no'
        )
        self.assertEqual(
            obj.persons_company.initiated_activities,
            date(2015, 2, 3)
        )
        self.assertEqual(
            obj.fiscal_position,
            models.FiscalPosition.objects.get(name='Do No Easy')
        )
        self.assertEqual(
            obj.fiscal_address.street_address,
            'San Martín 1100'
        )
        self.assertEqual(
            obj.fiscal_address.floor_number,
            '1'
        )
        self.assertEqual(
            obj.fiscal_address.apartment_number,
            '2'
        )
        self.assertEqual(
            obj.fiscal_address.locality,
            Locality.objects.get(pk=2)
        )
        self.assertEqual(
            obj.fiscal_address.postal_code,
            '2000'
        )


class ContactInvoiceTestCase(APITestCase):
    """
    """
    fixtures = [
        'invoice/tests/fixtures/users.json',
        'invoice/tests/fixtures/geo.json',
        'invoice/tests/fixtures/invoicing.json',
        'invoice/tests/fixtures/companies.json'
    ]

    def setUp(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse('api:invoice:contactinvoice-list')
        data = {
            'contact_contact': {
                'persons_company': (
                    reverse(
                        'api:persons:company-detail',
                        args=[Company.objects.get(fantasy_name='IRONA').pk]
                    )
                ),
                'name': 'Tobias Riper',
                'birth_date': '1970-07-07',
                'born_in': reverse('api:geo:country-detail', args=[1]),
                'phone_numbers': '555444555,333222333',
                'extra_emails': (
                    'top@kek.com'
                ),
                'contact_type': 'I',
                'home_address': {
                    'street_address': '9 de Julio 2454',
                    'floor_number': '',
                    'apartment_number': '',
                    'locality': (
                        reverse('api:geo:locality-detail', args=[1])
                    ),
                    'postal_code': '3000'
                }
            },
            'legal_name': 'Tobias Riper',
            'fiscal_position': (
                reverse('api:invoice:fiscalposition-detail', args=[1])
            ),
            'fiscal_address': {
                'street_address': '9 de Julio 2454',
                'floor_number': '',
                'apartment_number': '',
                'locality': reverse('api:geo:locality-detail', args=[1]),
                'postal_code': '3000'
            }
        }
        self.response = self.client.post(url, data)

    def tearDown(self):
        models.ContactInvoice.objects.filter(
            contact_contact__name='Riper Tobias'
        ).delete()
        Contact.objects.filter(name='Riper Tobias').delete()

    def test_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ContactInvoice.objects.count(), 1)

    def test_correctness(self):
        obj = models.ContactInvoice.objects.get(
            contact_contact__name='Tobias Riper'
        )
        self.assertEqual(
            obj.contact_contact.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            obj.contact_contact.name,
            'Tobias Riper'
        )
        self.assertEqual(
            obj.contact_contact.birth_date,
            date(1970, 7, 7)
        )
        self.assertEqual(
            obj.contact_contact.born_in,
            Country.objects.get(pk=1)
        )
        self.assertEqual(
            obj.contact_contact.phone_numbers,
            '555444555,333222333'
        )
        self.assertEqual(
            obj.contact_contact.extra_emails,
            'top@kek.com'
        )
        self.assertEqual(
            obj.contact_contact.contact_type,
            'I'
        )
        self.assertEqual(
            obj.contact_contact.home_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.contact_contact.home_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.contact_contact.home_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.contact_contact.home_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.contact_contact.home_address.postal_code,
            '3000'
        )
        self.assertEqual(
            obj.legal_name,
            'Tobias Riper'
        )
        self.assertEqual(
            obj.fiscal_position,
            models.FiscalPosition.objects.get(name='Do Easy')
        )
        self.assertEqual(
            obj.fiscal_address.street_address,
            '9 de Julio 2454'
        )
        self.assertEqual(
            obj.fiscal_address.floor_number,
            ''
        )
        self.assertEqual(
            obj.fiscal_address.apartment_number,
            ''
        )
        self.assertEqual(
            obj.fiscal_address.locality,
            Locality.objects.get(pk=1)
        )
        self.assertEqual(
            obj.fiscal_address.postal_code,
            '3000'
        )

    def test_update(self):
        admin = User.objects.get(username='admin')
        self.client.force_authenticate(user=admin)
        url = reverse(
            'api:invoice:contactinvoice-detail',
            args=[
                models.ContactInvoice.objects.get(
                    contact_contact__name='Tobias Riper'
                ).pk
            ]
        )
        data = {
            'contact_contact': {
                'persons_company': (
                    reverse(
                        'api:persons:company-detail',
                        args=[Company.objects.get(fantasy_name='IRONA').pk]
                    )
                ),
                'name': 'Riper Tobias',
                'birth_date': '1980-09-09',
                'born_in': reverse('api:geo:country-detail', args=[2]),
                'phone_numbers': '123456',
                'extra_emails': (
                    'kek@top.com'
                ),
                'contact_type': 'C',
                'home_address': {
                    'street_address': 'San Martín 1100',
                    'floor_number': '1',
                    'apartment_number': '2',
                    'locality': (
                        reverse('api:geo:locality-detail', args=[2])
                    ),
                    'postal_code': '2000'
                }
            },
            'legal_name': 'Riper Tobias',
            'fiscal_position': (
                reverse('api:invoice:fiscalposition-detail', args=[2])
            ),
            'fiscal_address': {
                'street_address': 'San Martín 1100',
                'floor_number': '1',
                'apartment_number': '2',
                'locality': reverse('api:geo:locality-detail', args=[2]),
                'postal_code': '2000'
            }
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = models.ContactInvoice.objects.get(
            contact_contact__name='Riper Tobias'
        )
        self.assertEqual(
            obj.contact_contact.persons_company,
            Company.objects.get(fantasy_name='IRONA')
        )
        self.assertEqual(
            obj.contact_contact.name,
            'Riper Tobias'
        )
        self.assertEqual(
            obj.contact_contact.birth_date,
            date(1980, 9, 9)
        )
        self.assertEqual(
            obj.contact_contact.born_in,
            Country.objects.get(pk=2)
        )
        self.assertEqual(
            obj.contact_contact.phone_numbers,
            '123456'
        )
        self.assertEqual(
            obj.contact_contact.extra_emails,
            'kek@top.com'
        )
        self.assertEqual(
            obj.contact_contact.contact_type,
            'C'
        )
        self.assertEqual(
            obj.contact_contact.home_address.street_address,
            'San Martín 1100'
        )
        self.assertEqual(
            obj.contact_contact.home_address.floor_number,
            '1'
        )
        self.assertEqual(
            obj.contact_contact.home_address.apartment_number,
            '2'
        )
        self.assertEqual(
            obj.contact_contact.home_address.locality,
            Locality.objects.get(pk=2)
        )
        self.assertEqual(
            obj.contact_contact.home_address.postal_code,
            '2000'
        )
        self.assertEqual(
            obj.legal_name,
            'Riper Tobias'
        )
        self.assertEqual(
            obj.fiscal_position,
            models.FiscalPosition.objects.get(name='Do No Easy')
        )
        self.assertEqual(
            obj.fiscal_address.street_address,
            'San Martín 1100'
        )
        self.assertEqual(
            obj.fiscal_address.floor_number,
            '1'
        )
        self.assertEqual(
            obj.fiscal_address.apartment_number,
            '2'
        )
        self.assertEqual(
            obj.fiscal_address.locality,
            Locality.objects.get(pk=2)
        )
        self.assertEqual(
            obj.fiscal_address.postal_code,
            '2000'
        )
