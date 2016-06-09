from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounting.models import Transaction
from contact.models import Contact
from persons.models import Company, PhysicalAddress


class FiscalPosition(models.Model):
    """
    A fiscal position is a classification given by a government to an
    individual or a company, which categorizes them into a tax-paying class.
    """
    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True
    )
    code = models.SlugField(
        _('code'),
        max_length=15,
        default="",
        blank=True,
        help_text=_("Some local official electronic systems handle "
                    "specific codes.")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('fiscal position')
        verbose_name_plural = _('fiscal positions')
        default_permissions = ('view', 'add', 'change', 'delete')


class CompanyInvoice(models.Model):
    """
    You need to define at least one to start invoicing, but you can add
    as many as you need.
    This is an extension of 'persons.models.Company'.
    """
    persons_company = models.OneToOneField(
        Company,
        verbose_name=_('company')
    )
    fiscal_position = models.ForeignKey(
        FiscalPosition,
        on_delete=models.PROTECT,
        verbose_name=_('fiscal position'),
        related_name='companies',
        related_query_name='company',
        blank=True,
        null=True,
        help_text=_("Certain countries require a fiscal position for "
                    "its taxpayers.")
    )
    fiscal_address = models.ForeignKey(
        PhysicalAddress,
        verbose_name=_('fiscal address'),
        related_name='+',
        related_query_name='+',
        blank=True,
        null=True
    )
    contacts = models.ManyToManyField(
        Contact,
        verbose_name=_('contacts'),
        related_name='companies',
        related_query_name='company',
        blank=True
    )

    def __str__(self):
        return self.persons_company.name

    class Meta:
        verbose_name = _('company')
        verbose_name_plural = _('companies')
        default_permissions = ('view', 'add', 'change', 'delete')


class ContactInvoice(models.Model):
    """
    Contact extension by Invoice.
    """
    contact_contact = models.OneToOneField(
        Contact,
        verbose_name=_('contact')
    )
    fiscal_position = models.ForeignKey(
        FiscalPosition,
        verbose_name=_('fiscal position'),
        related_name='contacts',
        related_query_name='contact',
        help_text=_("Certain countries require a fiscal position for "
                    "its taxpayers.")
    )
    fiscal_address = models.ForeignKey(
        PhysicalAddress,
        verbose_name=_('fiscal address'),
        related_name='+',
        related_query_name='+'
    )

    def __str__(self):
        return self.contact_contact.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        default_permissions = ('view', 'add', 'change', 'delete')


class VAT(models.Model):
    """
    VAT is a type of tax to consumption. Every country has it.
    """
    name = models.CharField(
        _('name'),
        max_length=15,
        unique=True,
        help_text=_("i.e. 8%")
    )
    code = models.SlugField(
        _('code'),
        max_length=15,
        default="",
        blank=True,
        help_text=_("Some local official electronic systems handle "
                    "specific codes.")
    )
    tax = models.FloatField(
        _('tax'),
        help_text=_("A value between 0.00 and 1.00"),
        validators=[MinValueValidator(0.00), MaxValueValidator(1.00)]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('VAT')
        verbose_name_plural = _('VATs')
        default_permissions = ('view', 'add', 'change', 'delete')


class Product(models.Model):
    """
    A basic product. It could also be a service.
    See other modules like 'sales' for more advanced products.
    """
    company = models.ForeignKey(
        Company,
        verbose_name=_('company'),
        related_name='products',
        related_query_name='product'
    )
    name = models.CharField(
        _('name'),
        max_length=150,
        help_text=_("It could also be a service.")
    )
    suggested_price = models.DecimalField(
        _('suggested price'),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vat = models.ForeignKey(
        VAT,
        verbose_name=_('VAT'),
        related_name='products',
        related_query_name='product'
    )

    def __str__(self):
        return "%(name)s" % {'name': self.name}

    class Meta:
        unique_together = (('company', 'name'), )
        index_together = [['company', 'name'], ]
        verbose_name = _('product')
        verbose_name_plural = _('products')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceLine(models.Model):
    """
    An invoice is composed of lines or entries, which have a product,
    a price and a quantity.
    """
    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
        related_name='invoice_lines',
        related_query_name='invoice_line'
    )
    product_price_override = models.DecimalField(
        _('product price'),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product_vat_override = models.ForeignKey(
        VAT,
        verbose_name=_('VAT override'),
        related_name='invoice_lines',
        related_query_name='invoice_line',
        blank=True,
        null=True
    )
    product_discount = models.FloatField(
        _('product discount'),
        default=0.00,
        blank=True,
        help_text=_("A number between 0.00 and 1.00")
    )
    quantity = models.PositiveIntegerField(
        _('quantity'),
        default=1
    )

    def __str__(self):
        return "%(product)s x %(quantity)s" % {
            'product': self.product,
            'quantity': self.quantity
        }

    class Meta:
        verbose_name = _('invoice line')
        verbose_name_plural = _('invoice lines')
        default_permissions = ('view', 'add', 'change', 'delete')


class InvoiceType(models.Model):
    """
    Government defined invoice types.
    """
    name = models.CharField(
        _('name'),
        max_length=150
    )
    code = models.SlugField(
        _('code'),
        max_length=15,
        default="",
        blank=True,
        help_text=_("Some local official electronic systems handle "
                    "specific codes.")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('invoice type')
        verbose_name_plural = _('invoice types')
        default_permissions = ('view', 'add', 'change', 'delete')


INVOICE_STATUSTYPE_DRAFT = 'D'
INVOICE_STATUSTYPE_SENT = 'S'
INVOICE_STATUSTYPE_PAID = 'P'
INVOICE_STATUSTYPE_CANCELED = 'C'
INVOICE_STATUS_TYPES = (
    (INVOICE_STATUSTYPE_DRAFT, _('Draft')),
    (INVOICE_STATUSTYPE_SENT, _('Sent')),
    (INVOICE_STATUSTYPE_PAID, _('Paid')),
    (INVOICE_STATUSTYPE_CANCELED, _('Canceled'))
)


class Invoice(models.Model):
    """
    The invoices themselves.
    """
    invoice_company = models.ForeignKey(
        CompanyInvoice,
        verbose_name=_('company'),
        related_name='invoices',
        related_query_name='invoice',
        db_index=True
    )
    contacts = models.ManyToManyField(
        Contact,
        verbose_name=_('contacts'),
        related_name='invoices',
        related_query_name='invoice'
    )
    number = models.BigIntegerField(
        _('number')
    )
    invoice_lines = models.ManyToManyField(
        InvoiceLine,
        verbose_name=_('invoice lines'),
        related_name='+',
        related_query_name='invoice'
    )
    invoice_type = models.ForeignKey(
        InvoiceType,
        verbose_name=_('invoice type'),
        related_name='invoices',
        related_query_name='invoice',
        blank=True,
        null=True
    )
    invoice_date = models.DateField(
        _('date'),
        help_text=_("Not necessarily today.")
    )
    status = models.CharField(
        _('status'),
        max_length=1,
        choices=INVOICE_STATUS_TYPES,
        default=INVOICE_STATUSTYPE_DRAFT
    )
    subtotal = models.DecimalField(
        _('subtotal'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_("Total without taxes.")
    )
    total = models.DecimalField(
        _('total'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_("Subtotal plus taxes.")
    )
    notes = models.TextField(
        _('notes'),
        blank=True,
        default=""
    )
    transaction = models.ForeignKey(
        Transaction,
        verbose_name=_('transaction'),
        related_name='+',
        related_query_name='+',
        blank=True,
        null=True
    )

    def __str__(self):
        return "%(invoice_company)s : %(number)s" % {
            'invoice_company': self.invoice_company.persons_company.name,
            'number': self.number
        }

    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        default_permissions = ('view', 'add', 'change', 'delete')
