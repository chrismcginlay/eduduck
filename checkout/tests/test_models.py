from django.test import TestCase

from ..models import Fee

class FeeModelTests(TestCase):
    """Test the models used to represent fees"""

    def test_fee_create(self):
        fee = Fee()
        assert(Fee)
