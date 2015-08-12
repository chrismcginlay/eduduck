from django.test import TestCase

from ..models import PricedItem 

class PricedItemModelTests(TestCase):
    """Test the models used to represent fees"""

    def test_PricedItem_create(self):
        fee = PricedItem()
        assert(fee)
