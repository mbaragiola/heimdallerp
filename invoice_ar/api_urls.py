from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from invoice_ar import views
from rest_framework_proxy.views import ProxyView

router = DefaultRouter()
router.register(r'contacts', views.ContactInvoiceARViewSet)
router.register(r'companies', views.CompanyInvoiceARViewSet)
router.register(r'pointsofsale', views.PointOfSaleViewSet)
router.register(r'concepttypes', views.ConceptTypeViewSet)
router.register(r'invoices', views.InvoiceARViewSet)
router.register(
    r'invoiceshavevatsubtotals',
    views.InvoiceARHasVATSubtotalViewSet
)

app_name = 'invoice_ar'
urlpatterns = [
    url(
        r'^afipws/cuit/(?P<cuit>[0-9]+)/$',
        ProxyView.as_view(source='sr-padron/v2/persona/%(cuit)s'),
        name='afipws-cuit'
    ),
    url(
        r'^afipws/dni/(?P<dni>[0-9]+)/$',
        ProxyView.as_view(source='sr-padron/v2/personas/%(dni)s'),
        name='afipws-dni'
    ),
    url(
        r'^concepttypes/(?P<pk>\d+)/invoices/$',
        views.InvoicesByConceptTypeList.as_view(),
        name='concepttype-invoices'
    ),
    url(
        r'^contacts/(?P<pk>\d+)/invoices/$',
        views.InvoicesByContactList.as_view(),
        name='contactinvoicear-invoices'
    ),
    url(
        r'^companies/(?P<pk>\d+)/invoices/$',
        views.InvoicesByCompanyList.as_view(),
        name='companyinvoicear-invoices'
    ),
    url(
        r'^pointsofsale/(?P<pk>\d+)/invoices/$',
        views.InvoicesByPointOfSaleList.as_view(),
        name='pointofsale-invoices'
    ),
    url(r'^', include(router.urls)),
]
