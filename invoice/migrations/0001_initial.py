# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 22:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persons', '0001_initial'),
        ('contact', '0001_initial'),
        ('accounting', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_name', models.CharField(blank=True, default='', max_length=200, verbose_name='legal name')),
                ('default_invoice_credit_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='accounting.Account', verbose_name='default invoice credit account')),
                ('default_invoice_debit_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='accounting.Account', verbose_name='default invoice debit account')),
                ('fiscal_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='persons.PhysicalAddress', verbose_name='fiscal address')),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='ContactInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_name', models.CharField(max_length=200, verbose_name='legal name')),
                ('contact_contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contact.Contact', verbose_name='contact')),
                ('fiscal_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='+', to='persons.PhysicalAddress', verbose_name='fiscal address')),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='FiscalPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('code', models.SlugField(blank=True, default='', help_text='Some local official electronic systems handle specific codes.', max_length=15, verbose_name='code')),
            ],
            options={
                'verbose_name': 'fiscal position',
                'verbose_name_plural': 'fiscal positions',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField(blank=True, default=0, verbose_name='number')),
                ('invoice_date', models.DateField(help_text='Not necessarily today.', verbose_name='date')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('A', 'Accepted'), ('S', 'Sent'), ('P', 'Paid'), ('C', 'Canceled')], default='D', max_length=1, verbose_name='status')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, help_text='Total without taxes.', max_digits=12, verbose_name='subtotal')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, help_text='Subtotal plus taxes.', max_digits=12, verbose_name='total')),
                ('notes', models.TextField(blank=True, default='', verbose_name='notes')),
                ('invoice_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', related_query_name='invoice', to='invoice.CompanyInvoice', verbose_name='company')),
                ('invoice_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoices', related_query_name='invoice', to='invoice.ContactInvoice', verbose_name='contact')),
                ('invoice_credit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices_credit', related_query_name='invoice_credit', to='accounting.Account', verbose_name='invoice credit account')),
                ('invoice_debit_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices_debit', related_query_name='invoice_debit', to='accounting.Account', verbose_name='invoice debit account')),
            ],
            options={
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_sold', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='price sold')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='A number between 0.00 and 1.00', max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='discount')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
            ],
            options={
                'verbose_name': 'invoice line',
                'verbose_name_plural': 'invoice lines',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='InvoiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('code', models.SlugField(blank=True, default='', help_text='Some local official electronic systems handle specific codes.', max_length=15, verbose_name='code')),
            ],
            options={
                'verbose_name': 'invoice type',
                'verbose_name_plural': 'invoice types',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='It could also be a service.', max_length=150, verbose_name='name')),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='current price')),
                ('invoice_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', related_query_name='product', to='invoice.CompanyInvoice', verbose_name='company')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='VAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='i.e. 8%', max_length=15, unique=True, verbose_name='name')),
                ('code', models.SlugField(blank=True, default='', help_text='Some local official electronic systems handle specific codes.', max_length=15, verbose_name='code')),
                ('tax', models.DecimalField(decimal_places=2, help_text='A value between 0.00 and 1.00', max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='tax')),
            ],
            options={
                'verbose_name': 'VAT',
                'verbose_name_plural': 'VATs',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', related_query_name='product', to='invoice.VAT', verbose_name='VAT'),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='invoice_lines', related_query_name='invoice_line', to='invoice.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_lines',
            field=models.ManyToManyField(blank=True, related_name='_invoice_invoice_lines_+', related_query_name='invoice', to='invoice.InvoiceLine', verbose_name='invoice lines'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='invoices', related_query_name='invoice', to='invoice.InvoiceType', verbose_name='invoice type'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', related_query_name='invoice', to='accounting.Transaction', verbose_name='transaction'),
        ),
        migrations.AddField(
            model_name='contactinvoice',
            name='fiscal_position',
            field=models.ForeignKey(help_text='Certain countries require a fiscal position for its taxpayers.', on_delete=django.db.models.deletion.PROTECT, related_name='contacts', related_query_name='contact', to='invoice.FiscalPosition', verbose_name='fiscal position'),
        ),
        migrations.AddField(
            model_name='companyinvoice',
            name='fiscal_position',
            field=models.ForeignKey(blank=True, help_text='Certain countries require a fiscal position for its taxpayers.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='companies', related_query_name='company', to='invoice.FiscalPosition', verbose_name='fiscal position'),
        ),
        migrations.AddField(
            model_name='companyinvoice',
            name='persons_company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='persons.Company', verbose_name='company'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('invoice_company', 'name')]),
        ),
    ]
