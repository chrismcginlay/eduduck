#checkout/tests/test_views.py
from django.test import TestCase

class PricedItemViewTests(TestCase):

    def test_PricedItemList_view_200_OK(self):
        response = self.client.get('/priced_items/')
        self.assertEqual(response.status_code, 200)

         

