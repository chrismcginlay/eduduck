#Functional tests for attachment app

#http://chimera.labs.oreilly.com/books/1234000000754/ch01.html#_obey_the_testing_goat_do_nothing_until_you_have_a_test

from selenium import webdriver
from django.test import TestCase
from django.core.urlresolvers import resolve
from courses.views import lesson

class AuthorAddsAttachmentToLessonTests(TestCase):
    """Course author wants to add an attachment to an existing lesson"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_from_lesson_author_can_add_attachment(self):

        #The author or instructor, Clare, visits a lesson she is responsible for
        found = resolve('/courses/1/lesson/2/')
        self.assertEqual(found.func, lesson)

        self.browser.get('http://localhost:8000/courses/1/lesson/2/')

        #She is presented with a list of existing attachments in that lesson
        att_header = self.browser.find_element_by_css_selector(
            'H4.attachments').text()
        self.assertIn('Attachments', att_header)
        att_list = self.browser.find_element_by_css_selector('ol.attachments')
        self.assertNotEqual(0, len(att_list))

        #Next to the list, is the facility to add more attachment(s)
        file_selector_box = self.browser.find_element_by_id('id_new_att')
#        @TestCase.skip
#        self.assertEqual(
#                file_selector_box.get_attribute('placeholder'),
#                'Select a file to upload'
#        )
        #On selecting this, Clare is shown a form to upload an attachment
        #The form has appropriate fields, with attachment code being optional 
        #not depending on settings on course page
        #After uploading an attachment and submitting the form, Clare can see the new attachment in the list

        self.fail('Write this test')

