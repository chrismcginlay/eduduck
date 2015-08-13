from django.test import TestCase
from factories import PricedItemFactory, DummyModelFactory
from dummy_app.models import DummyModel
from ..models import PricedItem 

    
class PricedItemModelTests(TestCase):
    """Test the models used to represent fees"""

    def test_PricedItem_create(self):
        fee = PricedItem()
        import pdb; pdb.set_trace()
        dummy_model = DummyModel(name="Bob")
        fee.content_object=dummy_model
        assert(fee.pk)

    def test_via_factory(self):
        somefee = PricedItemFactory()
        self.assertEqual(somefee.fee_value, 4.5)
        self.assertEqual(somefee.notes, u'Wibble')
        self.assertEqual(somefee.currency, u'GBP')
        self.assertEqual(somefee.tax_rate, 0.2)
