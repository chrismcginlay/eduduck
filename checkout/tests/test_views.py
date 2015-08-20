#checkout/tests/test_views.py
from django.test import TestCase

from .factories import PricedItemFactory, PricedItemFactoryWithDefaults
from ..models import PricedItem 

class PricedItemListViewTests(TestCase):

    def test_PricedItemList_view_200_OK(self):
        response = self.client.get('/priced_items/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemList_view_uses_correct_template(self):
        response = self.client.get('/priced_items/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_list.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")

    def test_PricedItemList_view_shows_items(self):
        items = PricedItemFactory.create_batch(size=10)
        response = self.client.get('/priced_items/')
        self.assertContains(response, 'DummyModel object 4.50 USD')
        self.assertEqual(len(response.context['priceditem_list']), 10)


class PricedItemDetailViewTests(TestCase):

    def test_PricedItemDetail_view_200_OK(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 200)
        
    def test_PricedItemDetail_view_uses_correct_template(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_detail.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")

    def test_PricedItemDetail_view_has_correct_context(self):
        pitem = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(pitem, response.context['priceditem'])


class PricedItemCreateViewTests(TestCase):

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

    def test_PricedItemCreate_view_uses_correct_template(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/create/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_create.html')

    def test_PricedItemCreate_view_has_success_url(self):
        form_data = {
            'content_type':1,
            'object_id':1,
            'fee_value':1.5, 
            'currency':'GBP',
            'tax_rate':0.2,
            'notes':'Wibble'
        }
        response = self.client.post('/priced_items/create/', form_data)
        self.assertRedirects(response, '/priced_items/')

class PricedItemUpdateTests(TestCase):

    def test_PricedItemUpdate_view_200_OK(self):
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemUpdate_view_uses_correct_template(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_update.html')

    def test_PricedItemUpdate_view_submit_button_says_UPDATE(self):
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertContains(response, '<input type="submit" value="Update">')

class PricedItemDeleteTests(TestCase):

    def test_PricedItemDelete_view_GET_200_OK(self):
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemDelete_view_GET_uses_correct_template(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 200) #the object exists
        response = self.client.get('/priced_items/1/delete/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_confirm_delete.html')

    def test_PricedItemDelete_view_POST_deletes(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 200) # the object exists
        response = self.client.post('/priced_items/1/delete/')
        self.assertRedirects(response, '/priced_items/')
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 404) # object is gone
