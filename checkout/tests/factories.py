from factory.django import DjangoModelFactory
from factory import SubFactory
from ..models import Payment, PricedItem
from dummy_app.models import DummyModel

class DummyModelFactory(DjangoModelFactory):
    class Meta:
        model = DummyModel

    name = "Fubar Saunders"

class PricedItemFactoryWithDefaults(DjangoModelFactory):
    """Leaves most data members out, triggering model defaults"""
    class Meta:
        model = PricedItem

    content_object = SubFactory(DummyModelFactory)
    
class PricedItemFactory(DjangoModelFactory):
    class Meta:
        model = PricedItem

    content_object = SubFactory(DummyModelFactory)
    fee_value = 4.5
    tax_rate = 0.2  
    notes = u"Wibble"
    currency = PricedItem.USD

class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment


