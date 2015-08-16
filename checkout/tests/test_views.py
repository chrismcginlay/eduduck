#checkout/tests/test_views.py
from django.test import TestCase

from .factories import PricedItemFactory
from ..models import PricedItem 

class PricedItemViewTests(TestCase):

    def test_PricedItemList_view_200_OK(self):
        response = self.client.get('/priced_items/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemList_view_shows_items(self):
        items = PricedItemFactory.create_batch(size=10)
        response = self.client.get('/priced_items/')
        self.assertContains(response, 'DummyModel object 4.50 USD')
        self.assertEqual(len(response.context['priceditem_list']), 10)

    def test_PricedItemCreate_view_200_OK(self):
        response = self.client.get('/priced_items/create/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemCreate_view_fields(self):
        response = self.client.get('/priced_items/create/')
        self.assertTrue('content_type' in response.context['form'].fields)
        self.assertTrue('object_id' in response.context['form'].fields)
        self.assertTrue('fee_value' in response.context['form'].fields)
        self.assertTrue('currency' in response.context['form'].fields)
        self.assertTrue('tax_rate' in response.context['form'].fields)
        self.assertTrue('notes' in response.context['form'].fields)

    def test_PricedItemCreate_view_has_success_url(self):
        response = self.client.get('/priced_items/create/')
        self.faile("does this redirect?")
        import pdb; pdb.set_trace()

