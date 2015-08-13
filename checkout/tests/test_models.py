from django.test import TestCase
from factories import PricedItemFactory
from ..models import PricedItem 

    
class PricedItemModelTests(TestCase):
    """Test the models used to represent fees"""

    def test_PricedItem_create(self):
        fee = PricedItem()
        assert(fee)

    def test_via_factory(self):
        somefee = PricedItemFactory()
        import pdb; pdb.set_trace()
