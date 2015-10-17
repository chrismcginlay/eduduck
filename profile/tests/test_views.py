from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth.models import User

from checkout.tests.factories import (
    PaymentFactory,
    PricedItemFactoryWithDefaults,
)

from ..models import Profile
from ..forms import ProfileEditForm


class ProfileViewTests(TestCase):
    """Test behaviour of user 'profile' views"""

    profile1_data = {
        'user_tz':         "Europe/Paris",
        'accepted_terms':  True,
        'signature_line':  'Some catchy signature.',
        'description':     'Detailed multiline description.',
        'webpage':         'http://www.unpossible.info',
    }

    def setUp(self):
        self.user1 = User.objects.create_user(
            'bertie', 'bertie@example.com', 'bertword')
        self.user1.is_active = True
        self.user1.save()    
       
    def test_profile_has_correct_context(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/accounts/profile/')
        context_vars =  [
            'profile',
            'usercourses',
            'taughtcourses',
            'auth_via',
            'receipts',
        ]
        [self.assertTrue(x in response.context, x+' missing') for x in context_vars]

    def test_profile_has_element_for_avatar(self):
        """The user avatar is visible"""
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/accounts/profile/')
        self.assertIn('id_avatar', response.content, "Avatar missing")

    def test_profile(self):
        """Test response profile.views.profile"""
        
        #Not logged in, redirect.
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')

        #log in and check profile is available      
        login = self.client.login(username='bertie', password='bertword')
        self.assertTrue(login)
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        context_vars = ['profile', 'usercourses']
        [self.assertTrue(x in response.context, x+' missing')
            for x in context_vars]
        self.assertIn('Timezone', response.content, "Timezone not rendered")

        #check for existence of password change link
        self.assertIn('<a href="/accounts/password/change/">Change Password</a>', 
            response.content, "Password change link missing")

    def test_profile_has_courses_taught_and_taken(self):
        """ There should be an area for courses instructed or courses taken """
        
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/accounts/profile/')
        self.assertIn('id_courses_enrolled', response.content)
        self.assertIn('id_courses_taught', response.content)

    def test_profile_has_receipts_area(self):
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/accounts/profile/')
        self.assertIn('id_receipts', response.content)
        self.assertIn(
            'View a full receipt by selecting any payment',
            response.content
        )
    
    def test_profile_receipts_area_shows_receipts(self):
        priceditem = PricedItemFactoryWithDefaults()
        bertie = User.objects.get(username='bertie')
        payment = PaymentFactory(paying_user=bertie)
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/accounts/profile/')
        self.assertIn('id_receipt_1', response.content)

    def test_profile_receipt_summary_provides_link(self):
        """A link is provided to view the entire receipt details"""
        priceditem = PricedItemFactoryWithDefaults()
        bertie = User.objects.get(username='bertie')
        payment = PaymentFactory(paying_user=bertie)
        self.client.login(username='bertie', password='bertword')
        response = self.client.get('/accounts/profile/')
        target = '<td><a href=\'/priced_items/payment/{0}/\'>{0}</a></td>'
        target = target.format(payment.id)
        self.assertIn(target, response.content)

    def test_profile_edit(self):
        """Test response profile.views.edit"""
        
        #Not logged in, redirect.
        response = self.client.get('/accounts/profile/edit/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/edit/')  
        #log in and check profile is available      
        login = self.client.login(username='bertie', password='bertword')
        self.assertTrue(login)
        response = self.client.get('/accounts/profile/edit/')
        self.assertEqual(response.status_code, 200)
        context_vars = ['profile', 'form']
        [self.assertTrue(x in response.context, x+' missing')
            for x in context_vars]

        #check for existence of password change link
        self.assertIn('<a href="/accounts/password/change/">Change Password</a>', 
            response.content, "Password change link missing")
        
        #Test form with missing data
        response = self.client.post("/accounts/profile/edit/", 
            kwargs={
                'accepted_terms': "True",
                'signature_line': "Test",
                'description': "Test description",
                'webpage': "www.eduduck.com",
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['user_tz'].errors, 
            [u'This field is required.'])

        #Test form with no data
        response = self.client.post("/accounts/profile/edit/", kwargs={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['user_tz'].errors, 
            [u'This field is required.'])

        #Test form with complete data
        response = self.client.post("/accounts/profile/edit/", 
            kwargs={
                'user_tz': "US/Pacific",
                'accepted_terms': "True",
                'signature_line': "Test",
                'description': "Test description",
                'webpage': "www.eduduck.com",
            })
        self.assertEqual(response.status_code, 200)

        #Test form with junk data
        response = self.client.post("/accounts/profile/edit/", kwargs={
            'blast': "pants",})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['user_tz'].errors, 
            [u'This field is required.'])

    def test_profile_public(self):
        """Test response profile.public"""

        url = "/accounts/profile/{0}/public/".format(self.user1.profile.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context_vars = ['timezone', 'webpage', 'description']
        [self.assertTrue(x in response.context, x+' missing')
            for x in context_vars]
        not_in_context_vars = [
            'auth_via', 
            'usercourses', 
            'taughtcourses', 
            'receipts'
        ]
        [self.assertFalse(x in response.context, x+' ought not to be present')
            for x in not_in_context_vars]    

    def test_password_reset_reachable(self):
        url = "/accounts/password_reset/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_reachable(self):
        url = "/accounts/password_reset/done/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #Following is slightly orphaned here. Testing next redirect parameter in 
    #login view, which is otherwise not tested (part of django.contrib.auth)
    def test_131_social_auth_has_next_param_to_course_create(self):
        """Creating course when not authenticated redirects back to create"""
        response = self.client.get('/accounts/login/?next=/courses/create/%3Fcourse_short_name%3DGardening')
        needle1 = '<a href="/login/google-oauth2/?next=/courses/create/?course_short_name=Gardening"'
        needle2 = '<a href="/login/facebook/?next=/courses/create/?course_short_name=Gardening"'
        self.assertIn(needle1, response.content)
        self.assertIn(needle2, response.content)        
