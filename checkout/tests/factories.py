from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import utc
from factory import PostGenerationMethodCall, Sequence, SubFactory
from factory.django import DjangoModelFactory
from ..models import Payment, PricedItem
from dummy_app.models import DummyModel

class DummyModelFactory(DjangoModelFactory):
    class Meta:
        model = DummyModel

    name = "Fubar Saunders"

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: u"User{0}".format(n, "%03d"))
    first_name = username
    last_name = u"Smith"
    password = PostGenerationMethodCall('set_password', 'frog')

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

    paying_user = SubFactory(UserFactory)
    content_object = SubFactory(DummyModelFactory)
    datestamp = datetime.now().replace(tzinfo=utc)

