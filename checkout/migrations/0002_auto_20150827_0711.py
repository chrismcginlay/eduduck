# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import checkout.models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priceditem',
            name='fee_value',
            field=models.DecimalField(default=1.0, max_digits=7, decimal_places=2, validators=[checkout.models.validate_positive]),
        ),
        migrations.AlterField(
            model_name='priceditem',
            name='tax_rate',
            field=models.DecimalField(default=0.0, max_digits=4, decimal_places=3, validators=[checkout.models.validate_positive]),
        ),
    ]
