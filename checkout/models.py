#checkout/models.py
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

def validate_positive(value):
    if value < 0:
        raise ValidationError('{0} ought not to be negative'.format(value))

class PricedItem(models.Model):
    """A price, fee, or cost to be associated with an instance of any model
    
    Attributes:
        content_type    models.ForeignKey(ContentType)
        fee_value       Monetary value of (pretax) fee
        currency        One of a list of currencies, eg. USD, GBP etc.
        tax_rate        Percentage tax rate as a decimal eg. 15% = 0.15
        notes           Optional note, e.g. introductory price
    """
    
    CNY = 'CNY'
    GBP = 'GBP'
    EUR = 'EUR'
    USD = 'USD'
    CURRENCY_CODE_CHOICES = (
        (CNY, 'Chinese yuan'),
        (GBP, 'Pound sterling'),
        (EUR, 'Euro'),    
        (USD, 'United States dollar'),
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    fee_value = models.DecimalField(
        decimal_places=2, 
        max_digits=7,
        null=False,
        blank=False,
        validators=[validate_positive],
        default=1.00
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CODE_CHOICES,
        blank=False,
        default=GBP
    )
    tax_rate = models.DecimalField(
        decimal_places=3,
        max_digits=4,
        null=False,
        blank=False,
        default=0.0,
        validators=[validate_positive]
    )
    notes = models.CharField(max_length=255)
    
    def get_absolute_url(self):
        return u"/priced_items/{0}/".format(self.pk)


class Payment(models.Model):

    CNY = 'CNY'
    GBP = 'GBP'
    EUR = 'EUR'
    USD = 'USD'
    CURRENCY_CODE_CHOICES = (
        (CNY, 'Chinese yuan'),
        (GBP, 'Pound sterling'),
        (EUR, 'Euro'),    
        (USD, 'United States dollar'),
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    fee_value = models.DecimalField(
        decimal_places=2, 
        max_digits=7,
        null=False,
        blank=False,
        validators=[validate_positive],
        default=1.00
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CODE_CHOICES,
        blank=False,
        default=GBP
    )
    tax_rate = models.DecimalField(
        decimal_places=3,
        max_digits=4,
        null=False,
        blank=False,
        default=0.0,
        validators=[validate_positive]
    )
    paying_user = models.ForeignKey(User)
    datestamp = models.DateTimeField()
    method = models.TextField(default=u'Stripe')  
    transaction_fee = models.DecimalField(
        decimal_places=3,
        max_digits=4,
        null=False,
        blank=False,
        default=0.0,
        validators=[validate_positive]
    )
    test_mode = models.BooleanField(
        null=False,
        blank=False,
        default=True
    )
 
    def get_absolute_url(self):
        return u"/priced_items/payment/{0}/".format(self.pk)
