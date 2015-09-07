#checkout/tests/test_urls.py
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase
from .factories import (
    PaymentFactory,
    PricedItemFactory,
    PricedItemFactoryWithDefaults
)

class PricedItemUrlTests(TestCase):
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
        self.assertEqual(resolver.view_name, 'checkout:priceditem_detail')
        self.assertEqual(resolver.kwargs, {'pk':unicode(somefee.pk)})

    def test_PricedItemDelete(self):
        somefee = PricedItemFactoryWithDefaults()
        url = reverse('checkout:priceditem_delete', kwargs={'pk':somefee.pk})
        self.assertEqual(url, '/priced_items/1/delete/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_delete')
        self.assertEqual(resolver.kwargs, {'pk':unicode(somefee.pk)})

    def test_PricedItemUpdate(self):
        somefee = PricedItemFactoryWithDefaults()
        url = reverse('checkout:priceditem_update', kwargs={'pk':somefee.pk})
        self.assertEqual(url, '/priced_items/1/update/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:priceditem_update')
        self.assertEqual(resolver.kwargs, {'pk':unicode(somefee.pk)})

class PaymentUrlTests(TestCase):

    def test_PaymentList(self):
        url = reverse('checkout:payment_list')
        self.assertEqual(url, '/priced_items/payment/')
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:payment_list')

    def test_PaymentListForUser(self):
        a_payment = PaymentFactory()
        url = reverse(
            'checkout:payment_list_for_user', kwargs={'pk':a_payment.pk})
        self.assertEqual(
            url, 
            '/priced_items/payment/user/{0}/'.format(a_payment.paying_user.id)
        )
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, 'checkout:payment_list_for_user')
        self.assertEqual(resolver.kwargs, {'pk':unicode(a_payment.pk)})

    def test_PaymentListForObject(self):
        a_payment = PaymentFactory()
        object_id = a_payment.content_object.id
        ctype = a_payment.content_type_id
        url = reverse(
            'checkout:payment_list_for_object',
            kwargs={'content_type_id':ctype, 'pk':object_id}
        )
        self.assertEqual(
            url, '/priced_items/payment/object_type/{0}/object/{1}/'.format(
                ctype, a_payment.object_id
        ))
        resolver = resolve(url)
        self.assertEqual(
            resolver.view_name, 'checkout:payment_list_for_object')
        self.assertEqual(
            resolver.kwargs, 
            {'content_type_id':unicode(ctype),'pk':unicode(object_id)} 
        )
