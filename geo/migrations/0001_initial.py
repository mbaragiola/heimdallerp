# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 11:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(default='en', max_length=2, verbose_name='language code')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name_plural': 'alternative names',
                'verbose_name': 'alternative name',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(db_index=True, max_length=2, unique=True, verbose_name='codename')),
                ('default_name', models.CharField(max_length=150, verbose_name='default name')),
                ('alternative_names', models.ManyToManyField(blank=True, related_name='_country_alternative_names_+', related_query_name='+', to='geo.AlternativeName', verbose_name='alternative names')),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name_plural': 'countries',
                'verbose_name': 'country',
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_name', models.CharField(max_length=150, verbose_name='default name')),
                ('alternative_names', models.ManyToManyField(blank=True, related_name='_locality_alternative_names_+', related_query_name='+', to='geo.AlternativeName', verbose_name='alternative names')),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name_plural': 'localities',
                'verbose_name': 'locality',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codename', models.CharField(blank=True, default='', max_length=4, verbose_name='codename')),
                ('default_name', models.CharField(max_length=150, verbose_name='default name')),
                ('alternative_names', models.ManyToManyField(blank=True, related_name='_region_alternative_names_+', related_query_name='+', to='geo.AlternativeName', verbose_name='alternative names')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='regions', related_query_name='region', to='geo.Country', verbose_name='country')),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
                'verbose_name_plural': 'regions',
                'verbose_name': 'region',
            },
        ),
        migrations.AddField(
            model_name='locality',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='localities', related_query_name='locality', to='geo.Region', verbose_name='region'),
        ),
    ]
