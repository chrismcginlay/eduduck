from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from factories import (
    PricedItemFactory, 
    PricedItemFactoryWithDefaults,
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
        fee = PricedItem(
            fee_value=1.2,
            tax_rate = 0.2,
            currency = PricedItem.GBP,
            notes = "Test note",
            content_object = dummy_instance,
        )
        fee.save()

class PricedItemModelTests2(TestCase):
    """Test models representing fees, with factory_boy"""

    def test_defaults(self):
        somefee = PricedItemFactoryWithDefaults()
        self.assertEqual(somefee.currency, PricedItem.GBP)

    def test_model_with_sane_values(self):
        somefee = PricedItemFactory()
        self.assertEqual(somefee.fee_value, 4.5)
        self.assertEqual(somefee.notes, u'Wibble')
        self.assertEqual(somefee.currency, PricedItem.USD)
        self.assertEqual(somefee.tax_rate, 0.2)
        somefee.clean()
    
    def test_out_of_bounds_raises_exceptions(self):
        somefee = PricedItemFactory.create()
        with self.assertRaises(ValidationError):
            somefee.fee_value = -0.3
            import pdb; pdb.set_trace()
            somefee.clean_fields()
        with self.assertRaises(ValidationError):
            somefee.tax_rate = -0.3
            somefee.full_clean()

