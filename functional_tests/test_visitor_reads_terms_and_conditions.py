from selenium import webdriver

from .base import FunctionalTest

class VisitorViewsAllTermsAndConditions(FunctionalTest):

    def test_all_terms_pages_are_reachable(self):
        # A casual visitor, Fred, not logged in, visits eduduck.com
        self.browser.get(self.server_url)
        # They see a link to Terms and Conditions in the menu
        menu = self.browser.find_element_by_id('menu')
        tandc_link = menu.find_element_by_link_text('Terms')
        # This link takes Fred to an index page
        tandc_link.click() 
        # There is a breadcrumb Home > T&C
        breadcrumb = self.browser.find_element_by_id('id_breadcrumb')
        # 4 links are listed in the main content area
        items_expected = [
            'Privacy',
            'Browsing', 
            'Enrolling', 
            'Creating',
        ]
        # Each link takes the user to the corresponding detail page
        # with a suitably updated breadcrumb Home > T&C > Privacy.
        # Selecting T&C takes Fred back to the T&C index.
        self._checkChildItemsPresent(items_expected, 'id_breadcrumb')
        self._checkChildLinksWork('id_breadcrumb')
        # After reading everything, Fred selects the Home link in the
        # breadcrumb which takes him back to the eduduck.com homepage
        home = self.browser.find_element_by_id('id_home')
        home.click()
        self.assertEqual(self.browser.get_current_url, self.server_url) 
        
class LoggedInUserAcceptsTermsAndConditionsViaProfilePage(FunctionalTest):
    
    def test_profile_page_has_link_to_terms(self):
        # Helmi logs in and visits her profile page.
        # She sees that terms and conditions are mentioned
        # Following the link provided takes her to the T&C index
        self.browser.get(self.server_url)
        self._logUserIn('helmi', 'plate509')
        self.browser.get(self.server_url+'/accounts/profile/')
        tandc_link = self.browser.find_element_by_id('id_tandc_link')
        tandc_link.click()
        self.assertEqual(
            self.browser.get_current_url,
            self.server_url+'/terms/'
        )

class UserLogsInAndAcceptsTermsAndConditionsViaTaCIndexPage(FunctionalTest):
    
    def test_terms_index_provides_accept_link_appropriately(self):
        # Fred visits the site, but is not logged in
        # He goes to the terms and conditions page
        self.browser.get(self.server_url+'/terms/')
        # From here he sees a link to accept terms
        accept_link = self.browser.find_element_by_id('id_accept_terms')
        # Since he is not logged in, this takes him to login
        self.assertEqual(
            self.browser.get_current_url,
            self.server_url+'/accounts/login/'
        )
        # He logs in and is taken to the profile/edit page
        self._logUserIn('chris', 'chris')
        # Here he is able to accept/refect the terms and conditions
        self.assertEqual(
            self.browser.get_current_url,
            self.server_url+'/accounts/profile/edit/'
        )
