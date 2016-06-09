# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 20:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoice', '0001_initial'),
        ('contact', '0001_initial'),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(blank=True, default='', max_length=200, verbose_name='description')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_categories', related_query_name='product_category', to='persons.Company', verbose_name='company')),
            ],
            options={
                'verbose_name_plural': 'product categories',
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name': 'product category',
            },
        ),
        migrations.CreateModel(
            name='ProductSales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', max_length=500, verbose_name='description')),
                ('categories', models.ManyToManyField(blank=True, related_name='products', related_query_name='product', to='sales.ProductCategory', verbose_name='categories')),
                ('invoice_product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='invoice.Product', verbose_name='product')),
            ],
            options={
                'verbose_name_plural': 'products',
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_date', models.DateField(help_text='Not necessarily today.', verbose_name='date')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, help_text='Total without taxes.', max_digits=12, verbose_name='subtotal')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, help_text='Subtotal plus taxes.', max_digits=12, verbose_name='total')),
                ('notes', models.TextField(blank=True, default='', verbose_name='notes')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('SA', 'Saved'), ('SO', 'Sold'), ('C', 'Canceled')], default='D', max_length=2, verbose_name='status')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotations', related_query_name='quotation', to='persons.Company', verbose_name='company')),
                ('contacts', models.ManyToManyField(related_name='quotations', related_query_name='quotation', to='contact.Contact', verbose_name='contacts')),
            ],
            options={
                'verbose_name_plural': 'quotations',
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name': 'quotation',
            },
        ),
        migrations.CreateModel(
            name='QuotationLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price_override', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='product price')),
                ('product_discount', models.FloatField(blank=True, default=0.0, help_text='A number between 0.00 and 1.00', verbose_name='product discount')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotation_lines', related_query_name='quotation_line', to='invoice.Product', verbose_name='product')),
                ('product_vat_override', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotation_lines', related_query_name='quotation_line', to='invoice.VAT', verbose_name='VAT override')),
            ],
            options={
                'verbose_name_plural': 'quotation lines',
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name': 'quotation line',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_date', models.DateField(help_text='Not necessarily today.', verbose_name='date')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, help_text='Total without taxes.', max_digits=12, verbose_name='subtotal')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, help_text='Subtotal plus taxes.', max_digits=12, verbose_name='total')),
                ('notes', models.TextField(blank=True, default='', verbose_name='notes')),
                ('status', models.CharField(choices=[('D', 'Draft'), ('S', 'Saved'), ('I', 'Invoiced'), ('C', 'Canceled')], default='D', max_length=1, verbose_name='status')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', related_query_name='sale', to='persons.Company', verbose_name='company')),
                ('contacts', models.ManyToManyField(related_name='sales', related_query_name='sale', to='contact.Contact', verbose_name='contacts')),
                ('quotation', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Quotation', verbose_name='quotation')),
            ],
            options={
                'verbose_name_plural': 'sales',
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name': 'sale',
            },
        ),
        migrations.CreateModel(
            name='SaleLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_price_override', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='product price')),
                ('product_discount', models.FloatField(blank=True, default=0.0, help_text='A number between 0.00 and 1.00', verbose_name='product discount')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_lines', related_query_name='sale_line', to='sales.ProductSales', verbose_name='product')),
                ('product_vat_override', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_lines', related_query_name='sale_line', to='invoice.VAT', verbose_name='VAT override')),
            ],
            options={
                'verbose_name_plural': 'sale lines',
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name': 'sale line',
            },
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_lines',
            field=models.ManyToManyField(related_name='_sale_sale_lines_+', related_query_name='sale', to='sales.SaleLine', verbose_name='sales lines'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='quotation_lines',
            field=models.ManyToManyField(related_name='_quotation_quotation_lines_+', related_query_name='quotation', to='sales.QuotationLine', verbose_name='quotation lines'),
        ),
        migrations.AlterUniqueTogether(
            name='productcategory',
            unique_together=set([('company', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='productcategory',
            index_together=set([('company', 'name')]),
        ),
    ]
