#checkout/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from .factories import PricedItemFactory, PricedItemFactoryWithDefaults

class UrlTests(TestCase):
    def test_PricedItemList(self):
        url = reverse('checkout:priceditem_list')
        self.assertEqual(url, '/priced_items/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_list')

    def test_PricedItemCreate(self):
        url = reverse('checkout:priceditem_create')
        self.assertEqual(url, '/priced_items/create/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_create')

    def test_PricedItemDetail(self):
        somefee = PricedItemFactoryWithDefaults()
        url = reverse('checkout:priceditem_detail', kwargs={'pk':somefee.pk})
        self.assertEqual(url, '/priced_items/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_create')
        self.assertEqual(resolver.kwargs, {'pk': somefee.pk})

    def test_PricedItemDelete(self):
        somefee = PricedItemFactoryWithDefaults()
        url = reverse('checkout:priceditem_delete', kwargs={'pk':somefee.pk})
        self.assertEqual(url, '/priced_items/1/delete/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_delete')
        self.assertEqual(resolver.kwargs, {'pk': somefee.pk})

    def test_PricedItemUpdate(self):
        somefee = PricedItemFactoryWithDefaults()
        url = reverse('checkout:priceditem_update', kwargs={'pk':somefee.pk})
        self.assertEqual(url, '/priced_items/1/update/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_update')
        self.assertEqual(resolver.kwargs, {'pk': somefee.pk})
