import sys
from unittest import skip
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class FunctionalTest(LiveServerTestCase):
    
    fixtures = [
        'auth_user.json', 
        'courses.json', 
        'lessons.json', 
        'outcome_lints.json', 
    ]

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
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
        
    def loguserin(self, user, passwd):
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