# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import checkout.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkout', '0002_auto_20150827_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('fee_value', models.DecimalField(default=1.0, max_digits=7, decimal_places=2, validators=[checkout.models.validate_positive])),
                ('currency', models.CharField(default=b'GBP', max_length=3, choices=[(b'CNY', b'Chinese yuan'), (b'GBP', b'Pound sterling'), (b'EUR', b'Euro'), (b'USD', b'United States dollar')])),
                ('tax_rate', models.DecimalField(default=0.0, max_digits=4, decimal_places=3, validators=[checkout.models.validate_positive])),
                ('datestamp', models.DateTimeField()),
                ('method', models.TextField(default='Stripe')),
                ('transaction_fee', models.DecimalField(default=0.0, max_digits=4, decimal_places=3, validators=[checkout.models.validate_positive])),
                ('test_mode', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('paying_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
