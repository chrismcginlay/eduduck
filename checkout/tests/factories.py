import factory
from ..models import PricedItem
from dummy_app.models import DummyModel

class DummyModelFactory(factory.Factory):
    class Meta:
        model = DummyModel

    name = "Fubar Saunders"


class PricedItemFactory(factory.Factory):
    class Meta:
        model = PricedItem

    content_object = factory.SubFactory(DummyModelFactory)
    fee_value = 4.5
    tax_rate = 0.2  
    notes = u"Wibble"
