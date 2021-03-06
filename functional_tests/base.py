import sys
from urllib import unquote
from django.contrib.contenttypes.models import ContentType 
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from checkout.models import PricedItem
from courses.models import Course

class FunctionalTest(LiveServerTestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome_lints.json', 
        'videos.json',
        'attachments.json',
    ]

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                fixtures = []   #no fixtures for testing liveserver staging
                return
        LiveServerTestCase.setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            LiveServerTestCase.tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        #TODO get rid of this once factory_boy has replaced fixtures
        courses = Course.objects.all()
        course_type = ContentType.objects.get_for_model(Course)
        #ensure each course has a corresponding PricedItem
        for course in courses:
            priced_item = PricedItem.objects.get_or_create(
                content_type_id=course_type.id, object_id=course.pk)

    def tearDown(self):
        self.browser.quit()
        
    def _logUserOut(self):
        logout_link = self.browser.find_element_by_id('id_logout')
        self.assertTrue(logout_link)
        logout_link.find_element_by_tag_name('a').click()
        self.assertEqual(
            self.browser.current_url,
            self.server_url + '/accounts/logout/')
        
    def _logUserIn(self, user, passwd, next_url='/accounts/profile/'):
        if self.server_url + '/accounts/login/' not in self.browser.current_url:
            #Don't always click the login link; in case where a ?next redirect
            #parameter has been set and we are already on the login page.
            login_link = self.browser.find_element_by_id('id_login')
            self.assertTrue(login_link)
            login_link.find_element_by_tag_name('a').click()
        #We should now be on login page, either with or without ?next param
        self.assertIn(
            self.server_url + '/accounts/login/', self.browser.current_url)

        username_textarea = self.browser.find_element_by_id('id_username')
        password_textarea = self.browser.find_element_by_id('id_password')
        form = self.browser.find_element_by_tag_name('form')
        username_textarea.send_keys(user)
        password_textarea.send_keys(passwd)
        form.submit()
        self.assertEqual(
            self.browser.current_url,
            self.server_url + unquote(next_url))

    def _checkChildItemsPresent(self, items_expected, parent_element_id):
        """ Verify that the expected items are present in a parent element
        
        items_expected      A list of item texts (probably menu items)
        parent_element_id   Attribute id of the element containing the items
        """
        
        pe = self.browser.find_element_by_id(parent_element_id)
        anchors = pe.find_elements_by_tag_name('a')
        a_list = [a.text for a in anchors]
        for item in items_expected:
            try:
                self.assertTrue(item in a_list)
            except AssertionError:
                print "*** {0} not in {1} ***".format(item, parent_element_id)
                raise

    def _checkChildLinksWork(self, element_id):
        """ Run through all the child links of an element (e.g. a menu div) 
        and check they don't 404 """
        
        ##initially, I obtained the anchors outside the loop, however they go
        ##stale after browser back button. Hence the clunky loop index approach.
        number_of_anchors = len(self.browser.find_element_by_id(element_id).find_elements_by_tag_name('a'))
        for i in range(number_of_anchors):
            start_window = self.browser.current_window_handle
            anchor = self.browser.find_element_by_id(element_id).find_elements_by_tag_name('a')[i]
            url = anchor.get_attribute('href')
            if anchor.text == 'Logout':
                continue    #Clicking logout will ruin the rest of the menu test!
            anchor.click()
            ##Next get handle to opened window and switch to it
            open_windows = self.browser.window_handles
            self.browser.switch_to_window(open_windows[-1])
            self.assertEqual(url, self.browser.current_url)
            self.assertNotIn('Page Not Found', self.browser.title)
            self.assertNotIn('Page not found', self.browser.title)
            self.browser.back()
            self.browser.switch_to_window(start_window)
            if len(open_windows)>1:
                self.browser.close()  #close extra windows

    def _expand_all_collapsible_blocks(self):
        shades = self.browser.find_elements_by_xpath("//span[@class]['shade']")
        for shade in shades:
            shade.click()
              
