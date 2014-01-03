#Functional tests for attachment app

#http://chimera.labs.oreilly.com/books/1234000000754/ch01.html#_obey_the_testing_goat_do_nothing_until_you_have_a_test

from selenium import webdriver
from django.test import TestCase

class AuthorAddsAttachmentToLessonTests(TestCase):
    """Course author wants to add an attachment to an existing lesson"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_visit_lesson_and_be_offered_attachment_addition(self):
        """The author/instructor can add attachments to a lesson"""

        #The author or instructor visits a lesson they are responsible for
        #They are presented with a list of existing attachments in that lesson
        #They are given the facility to add more attachment(s)

        self.browser.get('http://localhost:8000')

        self.fail('Write this test')

