# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('fee_value', models.DecimalField(max_digits=7, decimal_places=2)),
                ('currency', models.CharField(default=b'GBP', max_length=3, choices=[(b'CNY', b'Chinese yuan'), (b'GBP', b'Pound sterling'), (b'EUR', b'Euro'), (b'USD', b'United States dollar')])),
                ('tax_rate', models.DecimalField(max_digits=4, decimal_places=3)),
                ('notes', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
