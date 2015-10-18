#checkout/tests/test_views.py
from django.test import TestCase

from .factories import (
    PaymentFactory,
    PricedItemFactory,
    PricedItemFactoryWithDefaults,
    UserFactory
)
from ..models import PricedItem 

class PricedItemListViewTests(TestCase):
    def test_PricedItemList_view_302_not_superuser(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        response = self.client.get('/priced_items/')
        self.assertEqual(response.status_code, 302)

    def test_PricedItemList_view_200_OK_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        response = self.client.get('/priced_items/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemList_view_uses_correct_template(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        response = self.client.get('/priced_items/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_list.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")

    def test_PricedItemList_view_shows_items(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        items = PricedItemFactory.create_batch(size=10)
        response = self.client.get('/priced_items/')
        self.assertContains(response, 'DummyModel object')
        self.assertEqual(len(response.context['priceditem_list']), 10)

    def test_PricedItemList_view_each_item_links_to_detail(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        item = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/')
        self.assertContains(
            response, '<a href="/priced_items/1/">1</a>', html=True)

class PricedItemDetailViewTests(TestCase):

    def test_PricedItemDetail_view_200_OK_for_logged_in_user(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemDetail_view_302_not_logged_in(self):
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 302)
        
    def test_PricedItemDetail_view_uses_correct_template_for_logged_in_user(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_detail.html')
        self.assertContains(
            response, "<h2 id='id_page_title'>")

    def test_PricedItemDetail_view_has_correct_context(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        pitem = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(pitem, response.context['priceditem'])


class PricedItemCreateViewTests(TestCase):

    def test_PricedItemCreate_view_200_OK_for_superuser(self):
        superuser = UserFactory(is_superuser=True,is_active=True)
        self.client.login(username=superuser.username, password='frog')
        response = self.client.get('/priced_items/create/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemCreate_view_302_not_superuser(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        response = self.client.get('/priced_items/create/')
        self.assertEqual(response.status_code, 302)

    def test_PricedItemCreate_view_fields(self):
        superuser = UserFactory(is_superuser=True,is_active=True)
        self.client.login(username=superuser.username, password='frog')
        response = self.client.get('/priced_items/create/')
        self.assertTrue('content_type' in response.context['form'].fields)
        self.assertTrue('object_id' in response.context['form'].fields)
        self.assertTrue('fee_value' in response.context['form'].fields)
        self.assertTrue('currency' in response.context['form'].fields)
        self.assertTrue('tax_rate' in response.context['form'].fields)
        self.assertTrue('notes' in response.context['form'].fields)

    def test_PricedItemCreate_view_uses_correct_template(self):
        PricedItemFactoryWithDefaults()
        superuser = UserFactory(is_superuser=True,is_active=True)
        self.client.login(username=superuser.username, password='frog')
        response = self.client.get('/priced_items/create/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_base_form.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_create_form.html')

    def test_PricedItemCreate_view_has_success_url(self):
        superuser = UserFactory(is_superuser=True,is_active=True)
        self.client.login(username=superuser.username, password='frog')
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

    def test_PricedItemUpdate_view_200_OK_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemUpdate_view_uses_correct_template_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_update_form.html')

    def test_PricedItemUpdate_view_submit_button_says_UPDATE_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertContains(
            response, '<input type="submit" value="Update">', html=True)
    
    def test_PricedItemUpdate_view_POST_redirects_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/update/')
        self.assertEqual(response.status_code, 200) # the object exists
        form_data = {
            'content_type':1,
            'object_id':1,
            'fee_value':1.5, 
            'currency':'GBP',
            'tax_rate':0.2,
            'notes':'Wibble'
        }
        response = self.client.post('/priced_items/1/update/', form_data)
        self.assertRedirects(response, '/priced_items/')

class PricedItemDeleteTests(TestCase):

    def test_PricedItemDelete_view_GET_200_OK_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/delete/')
        self.assertEqual(response.status_code, 200)

    def test_PricedItemDelete_view_GET_302_not_superuser(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        somefee = PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/delete/')
        self.assertEqual(response.status_code, 302)

    def test_PricedItemDelete_view_GET_uses_correct_template(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 200) #the object exists
        response = self.client.get('/priced_items/1/delete/')
        self.assertTemplateUsed(response, 'checkout/priceditem_base.html')
        self.assertTemplateUsed(response, 'checkout/priceditem_confirm_delete.html')

    def test_PricedItemDelete_view_has_submit_button(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/delete/')
        self.assertContains(
            response, '<input type="submit" value="Confirm">', html=True)

    def test_PricedItemDelete_view_POST_deletes(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        PricedItemFactoryWithDefaults()
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 200) # the object exists
        response = self.client.post('/priced_items/1/delete/')
        self.assertRedirects(response, '/priced_items/')
        response = self.client.get('/priced_items/1/')
        self.assertEqual(response.status_code, 404) # object is gone

class PaymentListViewTests(TestCase):

    def test_Payment_list_view_200_OK_for_superuser(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        a_payment = PaymentFactory()
        response = self.client.get('/priced_items/payment/')
        self.assertEqual(response.status_code, 200)

    def test_Payment_list_view_302_not_superuser(self):
        mortaluser = UserFactory(is_active=True)
        self.client.login(username=mortaluser.username, password='frog')
        a_payment = PaymentFactory()
        response = self.client.get('/priced_items/payment/')
        self.assertEqual(response.status_code, 302)

    def test_Payment_list_for_user_view_200_OK(self):
        a_payment = PaymentFactory()
        payer = a_payment.paying_user
        self.client.login(username=payer.username, password='frog') 
        response = self.client.get('/priced_items/payment/user/')
        self.assertEqual(response.status_code, 200)

    def test_Payment_list_for_object_view_200_OK(self):
        superuser = UserFactory(is_superuser=True, is_active=True)
        self.client.login(username=superuser.username, password='frog')
        a_payment = PaymentFactory()
        content_type_id = a_payment.content_type_id
        purchased_object_id = a_payment.object_id
        response = self.client.get(
            '/priced_items/payment/object_type/{0}/object/{1}/'.format(
                content_type_id, purchased_object_id
        )) 
        self.assertEqual(response.status_code, 200)

class PaymentDetailViewTests(TestCase):

    def test_Payment_detail_view_200_OK_for_paying_user(self):
        a_payment = PaymentFactory()
        payer = a_payment.paying_user
        self.client.login(username=payer.username, password='frog')
        response = self.client.get(a_payment.get_absolute_url())
        self.assertEqual(response.status_code, 200) #the object exists

    def test_Payment_detail_view_403_OK_for_other_user(self):
        someuser=UserFactory()
        a_payment = PaymentFactory()
        payer = a_payment.paying_user
        self.client.login(username=someuser.username, password='frog')
        response = self.client.get(a_payment.get_absolute_url())
        self.assertEqual(response.status_code, 403) 

    def test_Payment_detail_uses_correct_templates(self):
        a_payment = PaymentFactory()
        payer = a_payment.paying_user
        self.client.login(username=payer.username, password='frog')
        response = self.client.get(a_payment.get_absolute_url())
        self.assertEqual(response.status_code, 200) #the object exists
        self.assertTemplateUsed(response, 'checkout/payment_base.html')
        self.assertTemplateUsed(response, 'checkout/payment_detail.html')
