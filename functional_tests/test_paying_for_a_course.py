#functional_tests/test_paying_for_a_course.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class CanonicalWorkflow(FunctionalTest):

    def test_redirect_unpaid_course_fee_to_payment_mechanism(self):
        # Helmi is visiting the course page for 'Blender' but has not paid
        self.browser.get(self.server_url)
        self._logUserIn('helmi', 'plate509')
        self.browser.get(self.server_url+'/courses/1/')

        # The Enrol button shows a course fee
        enrol = self.browser.find_element_by_id('id_enrol_button')
        self.assertEqual(enrol.text, u'Enrol \xa31.00')

        # She accesses the first lesson free of charge, without enrolling
        first_lesson = self.browser.find_element_by_id('id_lesson1')
        first_lesson.click()
        page_title = self.browser.find_element_by_id('id_lesson_title')
        self.assertEqual(page_title.text, u'Lesson: What is Blender for?')

        # But the 2nd and later lessons pop up an payment overlay, which she
        # dismisses just now, being redirected to the course homepage.
        course1_url = "{0}/courses/1/".format(self.server_url)
        self.browser.get(course1_url)
        second_lesson = self.browser.find_element_by_id('id_lesson2')
        second_lesson.click()
       
        overlay = self.browser.find_element_by_id('id_payment_overlay')
        self.assertTrue(overlay.is_displayed()) 
        btn_cancel = self.browser.find_element_by_id('id_cancel_payment')
        btn_cancel.click()
        self.assertFalse(overlay.is_displayed())
        self.assertEqual(self.browser.current_url, course1_url)

        # Clicking on Enrol a javascript overlay pops up for Stripe Checkout
        enrol = self.browser.find_element_by_id('id_enrol_button')
        enrol.click()
        overlay = self.browser.find_element_by_id('id_payment_overlay')
        self.assertTrue(overlay.is_displayed()) 

        # Helmi pays for the course via Stripe (in TEST mode!)

        # The stripe payment overlay goes away and she returns to course page
        # Now, the Enrol button is gone.
        # And, she can access all the lessons.
        # Logging out and later, logging in again, her course access is still
        # available.
        # On her profile page, she can see which courses she has paid for, 
        # along with how much was paid and when.
        self.fail("Write now")

    def test_author_reviews_paid_enrolments_for_course(self):
        # Gordon has been organiser/instructor for a couple of courses
        # On his profile page he can see the two courses he's involved with.
        # Selecting one, he is taken to a page summarising his students' 
        # interactions on that course.
        # He can see the total number of enrolments
        # There is a section detailing total lesson views
        # And a list of enrolment payments made, along with date made.
        self.fail("Write now")
