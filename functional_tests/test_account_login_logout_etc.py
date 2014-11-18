from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest

class VisitorDecidesToSignIn(FunctionalTest):
    """Social signin facilities"""
    
    def test_signup_signin_workflow(self):
        # Roland makes his first visit to the site.
        # He sees the login/signup area.
        self.browser.get(self.server_url)
        login_link = self.browser.find_element_by_xpath(
            "//li[@id='id_login']/a[1]")
    
        # He hits the 'login/signup' option
        login_link.click()

        # This takes him to a page showing a number of options for social auth
        # replicated in two areas, one for login, one for signup.
        psa_url = self.server_url + '/accounts/login/'
        self.assertEqual(psa_url, self.browser.current_url)
        self.browser.find_element_by_id('id_signup_login_area')
        goal = self.browser.find_element_by_id('id_google_oauth2')
        self.browser.find_element_by_id('id_dropbox_oauth')
        self.browser.find_element_by_id('id_twitter_oauth2')
        self.browser.find_element_by_id('id_facebook_oauth2')
        
        ## CAREFUL - following these 3rd party authentications will have a
        ## side effect if browser is logged in to a service. 
        
        # Roland logs in ## JUST USE CHRIS/CHRIS until figure out mocking
        self._logUserIn('chris', 'chris')   
        
        # He is redirected to his profile page
        target_url = self.server_url + '/accounts/profile/'
        self.assertEqual(self.browser.current_url, target_url)
        
        # ...confirming his login method and other details
        self.browser.find_element_by_id('id_account_status')
        self.browser.find_element_by_id('id_courses_enrolled')
        self.browser.find_element_by_id('id_change_password')
        self.browser.find_element_by_id('id_courses_taught')
        self.browser.find_element_by_id('id_personal_details')

        # Returning to the homepage he sees that the social auth options area
        # now shows the method used to login.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_account_status')
        
        # ...and a link to his profile
        self.browser.find_element_by_id('id_profile_link')

        # Visiting the accounts/login page again; already logged in, so 
        # instead of login options he sees a message explaining that he is 
        # already logged in and a link to his profile page.
        self.browser.get(psa_url)
        self.browser.find_element_by_id('id_account_status')
        self.browser.find_element_by_id('id_profile_link')

        # He tries to login with google, but there is no record of an account
        #goal.click() # Mock this?
        self.fail("Unsure how to test 3rd party auth")
        # He is informed of this and redirected to signup.

        # Having signed up he is redirected to his account profile page.

        # Roland logs out, then logs back in again.


class NewVisitorDecidesToRegisterViaEmail(FunctionalTest):
    """Covers registration, profile page, logout and login"""
    
    def test_registration_profile_edit_logout_login(self):
        self.fail("Amend this for new auth")
        # Roland arrives on the site. He has not registered yet.
        # He sees the login option in the menu and the registration area on the 
        # main page.
        self.browser.get(self.server_url)
        self.assertTrue(self.browser.find_element_by_id('id_login'))
        self.assertTrue(self.browser.find_element_by_id('id_sign_up_form'))

        # Roland is so keen to register, he accidentally hits 'sign up'
        # without first entering a username
        signup_form = self.browser.find_element_by_id('id_sign_up_form')
        signup_form.submit()
        
        # He is taken to the accounts/register page & an error message appears:
        error = self.browser.find_element_by_css_selector('.errorlist')
        self.assertEqual(error.text, "This field is required.")

        # Roland now fills in a username and clicks 'Sign Up' button
        signup_form = self.browser.find_element_by_tag_name('form')
        username_textarea = signup_form.find_element_by_id('id_username')
        username_textarea.send_keys("Roland")
        ## Seems to be necessary to refind form (goes out of cache?)
        signup_form = self.browser.find_element_by_tag_name('form')
        signup_form.submit()

        # Since he didn't fill in an email address or password, the form is 
        # re-presented with the same username, but the error fields highlighted.
        username_textarea = self.browser.find_element_by_id('id_username')
        self.assertEqual(username_textarea.get_attribute('value'), "Roland")
        errors = self.browser.find_elements_by_css_selector('.errorlist')
        self.assertEqual(len(errors), 3) #There are 3 blank fields so far

        for error in errors:
            self.assertEqual(error.text, "This field is required.")
        
        # He enters email and password details, 
        email_textarea = self.browser.find_element_by_id('id_email')
        password1_textarea = self.browser.find_element_by_id('id_password1')
        password2_textarea = self.browser.find_element_by_id('id_password2')
        ## Use a public mailinator address to get the activation code
        email_textarea.send_keys('rolandtheeduducker@mailinator.com')
        password1_textarea.send_keys('wibble')
        password2_textarea.send_keys('wibble')
        
        # He re-submits the form, which passes validation. 
        # He is taken to the pending activation holding page_source
        signup_form = self.browser.find_element_by_tag_name('form')
        signup_form.submit()
        self.assertEqual(
            self.browser.current_url, 
            self.server_url + '/accounts/register/complete/')
        self.fail("implement the rest of this test")
        ## TODO The following would be nice to test. Need to figure out how to
        ## mock the confirmation email activation code.
        ## Could use mailinator or filebased backend for email.
        
"""
        # Roland is taken to his new user profile page. 
        # Here he sees the basic and extra details for his account...
        self.assertEqual(self.browser.current_url, '/accounts/profile/edit')
        
        # ...and with the possibility to change the default timezone, tagline etc.
        detail_edit_form = self.browser.find_element_by_id('id_edit_account')
        self.assertTrue(detail_edit_form)
        
        # The main page no longer shows the registration area
        self.fail("write me")
        
        # After spending some more time on the site, he then logs out.
        pass

        # The menu entry reverts to 'login' and the register area appears again.
        self.fail("write me")
        
        # Roland decides to login again. Pressing the login button, he is taken to
        # the login page
        self.loguserin('Roland', 'wibble')
"""

class RegisteredUserLogsIn(FunctionalTest):
    """ Covers the login/logout process """

    def test_login_logout(self):
        # Chris visits the site (cue music)
        self.browser.get(self.server_url)

        # He is not logged in, so sees the login option in the menu
        self._logUserIn('chris', 'chris')

        #This takes him to his profile area
        self.assertEqual(
            self.browser.current_url,
            self.server_url + '/accounts/profile/')

        # Since he is logged in, the menu now shows 'logout' in place of login. 
        try:
            self.browser.find_element_by_id('id_login')
        except NoSuchElementException:
            pass
        self.assertTrue(self.browser.find_element_by_id('id_logout'))        

        # Also, a link to his profile, 
        profile_link = self.browser.find_element_by_id('id_profile')
        self.assertTrue(profile_link)

