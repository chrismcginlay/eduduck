#checkout/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

class UrlTests(TestCase):
    def test_PricedItemList(self):
        url = reverse('checkout:priceditem_list')
        self.assertEqual(url, '/priced_items/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_list')
