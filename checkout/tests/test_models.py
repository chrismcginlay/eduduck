from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, TransactionTestCase
from django.utils.timezone import utc
from factories import (
    PaymentFactory,
    PricedItemFactory, 
    PricedItemFactoryWithDefaults,
    UserFactory,
    DummyModelFactory
)
from dummy_app.models import DummyModel
from ..models import PricedItem 

    
class PricedItemModelTests1(TransactionTestCase):
    """Test the models used to represent fees, w/o factory_boy"""

    # Manually test saving in database, requires TransactionTestCase
    def test_PricedItem_create_and_save(self):
        dummy_instance = DummyModel(name="Florence")
        dummy_instance.save()
        somefee = PricedItem(
            fee_value=1.2,
            tax_rate = 0.2,
            currency = PricedItem.GBP,
            notes = "Test note",
            content_object = dummy_instance,
        )
        somefee.save()
        self.assertTrue(somefee.pk)

class PricedItemModelTests2(TestCase):
    """Test models representing fees, with factory_boy"""

    def test_defaults(self):
        somefee = PricedItemFactoryWithDefaults()
        self.assertEqual(somefee.currency, PricedItem.GBP)
        self.assertTrue(somefee.pk)

    def test_model_with_sane_values(self):
        somefee = PricedItemFactory()
        self.assertEqual(somefee.fee_value, 4.5)
        self.assertEqual(somefee.notes, u'Wibble')
        self.assertEqual(somefee.currency, PricedItem.USD)
        self.assertEqual(somefee.tax_rate, 0.2)
        self.assertTrue(somefee.pk)
        somefee.clean()
    
    def test_out_of_bounds_fee_value_raises_exceptions(self):
        somefee = PricedItemFactory()
        with self.assertRaises(ValidationError):
            somefee.fee_value = -0.3
            somefee.full_clean()

    def test_out_of_bounds_tax_rate_raises_exceptions(self):
        somefee = PricedItemFactory()
        with self.assertRaises(ValidationError):
            somefee.tax_rate = -0.3
            somefee.full_clean()

    def test_bogus_currency_raises_exceptions(self):
        somefee = PricedItemFactory()
        with self.assertRaises(ValidationError):
            somefee.currency = 'potatoes'
            somefee.full_clean()

    def test_get_absolute_url(self):
        somefee = PricedItemFactoryWithDefaults()
        expected_url = '/priced_items/{0}/'.format(somefee.pk)
        gau = somefee.get_absolute_url()
        self.assertEqual(expected_url, gau)

class PaymentModelTests(TestCase):

    def test_model_with_sane_values(self):
        a_user = UserFactory()
        turing = datetime(1912, 6, 23, 12, 00, tzinfo=utc)
        a_payment = PaymentFactory(
            paying_user=a_user,
            tax_rate=Decimal(0.2),
            datestamp = turing,
            transaction_fee = Decimal(0.2),
        )
        self.assertEqual(a_payment.paying_user, a_user)
        dummy_model_type = ContentType.objects.get_for_model(DummyModel)
        self.assertEqual(a_payment.content_type, dummy_model_type)
        self.assertEqual(a_payment.fee_value, Decimal(1.00))
        self.assertEqual(a_payment.currency, u'GBP')
        self.assertEqual(a_payment.tax_rate, Decimal(0.2))
        self.assertEqual(
            a_payment.datestamp, turing)
        self.assertEqual(a_payment.method, u'Stripe')
        self.assertEqual(a_payment.transaction_fee, Decimal(0.20))
        self.assertEqual(a_payment.test_mode, True)

    def test_out_of_bounds_fee_value_raises_exceptions(self):
        a_payment = PaymentFactory()
        with self.assertRaises(ValidationError):
            a_payment.fee_value = -0.3
            a_payment.full_clean()

    def test_out_of_bounds_tax_rate_raises_exceptions(self):
        a_payment = PaymentFactory()
        with self.assertRaises(ValidationError):
            a_payment.tax_rate = -0.3
            a_payment.full_clean()

    def test_bogus_currency_raises_exceptions(self):
        a_payment = PaymentFactory()
        with self.assertRaises(ValidationError):
            a_payment.currency = 'potatoes'
            a_payment.full_clean()

    def test_get_absolute_url(self):
        a_payment = PaymentFactory()
        expected_url = '/priced_items/payment/{0}/'.format(a_payment.pk)
        gau = a_payment.get_absolute_url()
        self.assertEqual(expected_url, gau)
