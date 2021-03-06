from django.conf.urls import include, url

from contact import api_urls as contact_urls
from hr import api_urls as hr_urls
from geo import api_urls as geo_urls
from invoice import api_urls as invoice_urls
from invoice_ar import api_urls as invoicear_urls
from persons import api_urls as persons_urls
from accounting import api_urls as accounting_urls


urlpatterns = [
    url(
        r'^geo/',
        include(geo_urls, namespace='geo')
    ),
    url(
        r'^persons/',
        include(persons_urls, namespace='persons')
    ),
    url(
        r'contact/',
        include(contact_urls, namespace='contact')
    ),
    url(
        r'^hr/',
        include(hr_urls, namespace='hr')
    ),
    url(
        r'^invoice/',
        include(invoice_urls, namespace='invoice')
    ),
    url(
        r'^invoice_ar/',
        include(invoicear_urls, namespace='invoice_ar')
    ),
    url(
        r'^accounting/',
        include(accounting_urls, namespace='accounting')
    ),
]
