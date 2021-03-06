from rest_framework.serializers import (HyperlinkedIdentityField,
                                        HyperlinkedModelSerializer)

from invoice.serializers import ProductSerializer
from sales import models


class ProductCategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = (
            'url',
            'id',
            'persons_company',
            'name',
            'description'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:productcategory-detail'
            },
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            }
        }


class ProductSalesSerializer(HyperlinkedModelSerializer):
    invoice_product = ProductSerializer()
    categories = HyperlinkedIdentityField(
        view_name='api:sales:productsales-categories'
    )

    class Meta:
        model = models.ProductSales
        fields = (
            'url',
            'id',
            'invoice_product',
            'description',
            'categories'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:productsales-detail'
            }
        }


class QuotationLineSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.QuotationLine
        fields = (
            'url',
            'id',
            'product',
            'product_price_override',
            'product_vat_override',
            'product_discount',
            'quantity'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:quotationline-detail'
            },
            'product': {
                'view_name': 'api:invoice:product-detail'
            }
        }


class QuotationSerializer(HyperlinkedModelSerializer):
    quotation_lines = QuotationLineSerializer(many=True)

    class Meta:
        model = models.Quotation
        fields = (
            'url',
            'id',
            'persons_company',
            'contacts',
            'quotation_lines',
            'quotation_date',
            'notes',
            'subtotal',
            'total'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:quotation-detail'
            },
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            },
            'contacts': {
                'view_name': 'api:contact:contact-detail',
                'many': True
            }
        }


class SaleLineSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.SaleLine
        fields = (
            'url',
            'id',
            'product',
            'product_price_override',
            'product_vat_override',
            'product_discount',
            'quantity'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:saleline-detail'
            },
            'product': {
                'view_name': 'api:invoice:product-detail'
            }
        }


class SaleSerializer(HyperlinkedModelSerializer):
    sale_lines = SaleLineSerializer(many=True)

    class Meta:
        model = models.Sale
        fields = (
            'url',
            'id',
            'persons_company',
            'contacts',
            'sale_lines',
            'sale_date',
            'notes',
            'subtotal',
            'total',
            'status'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'api:sales:sale-detail'
            },
            'persons_company': {
                'view_name': 'api:persons:company-detail'
            },
            'contacts': {
                'view_name': 'api:contact:contact-detail',
                'many': True
            }
        }
