import sys
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class FunctionalTest(LiveServerTestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome_lints.json', 
        'videos.json',
        'attachments.json'
    ]

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                self.fixtures = []   #no fixtures for testing liveserver staging
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

    def tearDown(self):
        self.browser.quit()
        
    def _logUserIn(self, user, passwd):
        login_link = self.browser.find_element_by_id('id_login')
        self.assertTrue(login_link)
        login_link.find_element_by_tag_name('a').click()
        self.assertEqual(
            self.browser.current_url, 
            self.server_url + '/accounts/login/')
        username_textarea = self.browser.find_element_by_id('id_username')
        password_textarea = self.browser.find_element_by_id('id_password')
        form = self.browser.find_element_by_tag_name('form')
        username_textarea.send_keys(user)
        password_textarea.send_keys(passwd)
        form.submit()
        self.assertEqual(
            self.browser.current_url,
            self.server_url + '/accounts/bio/')

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
