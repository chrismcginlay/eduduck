#functional_tests/test_paying_for_a_course.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class CanonicalWorkflow(FunctionalTest):

    def test_redirect_unpaid_course_fee_to_payment_mechanism(self):
        # Helmi is visiting the course page for 'Blender' but has not paid
        self.browser.get(self.server_url)
        self._logUserIn('helmi', 'plate509')
        course_url = "{0}/courses/2/".format(self.server_url)
        self.browser.get(course_url)

        # The Enrol button shows a course fee
        enrol = self.browser.find_element_by_id('id_enrol_button')
        self.assertEqual(enrol.text, u'Enrol \xa31.00')

        # She accesses the first lesson free of charge, without enrolling
        first_lesson = self.browser.find_element_by_id('id_lesson1')
        first_lesson.click()
        page_title = self.browser.find_element_by_id('id_lesson_title')
        self.assertEqual(page_title.text, u'Lesson: Structural Overview')

        # But the 2nd and later lessons redirect to the course homepage.
        self.browser.get(course_url)
        second_lesson = self.browser.find_element_by_id('id_lesson2')
        second_lesson.click()
        self.assertEqual(self.browser.current_url, course_url)

        # CLicking on Enrol or Pay and the javascript overlay pops up
        enrol = self.browser.find_element_by_id('id_enrol_button')
        enrol.click()
        # The overlay for payment is in an iframe
        self.browser.switch_to_frame(1)
        overlay = self.browser.find_element_by_class_name(
            "stripeInFrame")
        self.assertTrue(overlay.is_displayed()) 
        btn_cancel = self.browser.find_element_by_xpath(
            "//a[@class='close right']")
        # Cancelling the payment overlay, Helmi returns to the enrol button
        btn_cancel.click()
        self.browser.switch_to_default_content()
        enrol = self.browser.find_element_by_id('id_enrol_button')
        
        # Clicking on Enrol the javascript overlay pops up again
        self.browser.implicitly_wait(10)
        enrol.click()
        
        # Helmi pays for the course via Stripe (in TEST mode!)
        self.browser.switch_to_frame(2)    
        testmode = self.browser.find_element_by_xpath(
            "//a[@class='testMode']")
        self.assertEqual(testmode.text, 'TEST MODE')

        self.browser.switch_to_default_content() # back to main page
        self.browser.switch_to_frame(1)
        overlay = self.browser.find_element_by_xpath(
            "//body[@class='stripeInFrame appView iframe desktop']")
        self.assertTrue(overlay.is_displayed()) 
        email_input = self.browser.find_element_by_xpath(
            "//input[@id='email']")
        card_number_input = self.browser.find_element_by_xpath(
            "//input[@id='card_number']")
        card_exp_input = self.browser.find_element_by_xpath(
            "//input[@id='cc-exp']")
        card_cvc_input = self.browser.find_element_by_xpath(
            "//input[@id='cc-csc']")
        pay_button = self.browser.find_element_by_id('submitButton')
        check_val = pay_button.find_element_by_xpath("//span/span").text
        #verify correct balance to pay:
        self.assertEqual(check_val, u'Pay \xa31.00')  
     
        email_input.send_keys("chris@example.com")
        card_number_input.send_keys("4242")
        card_number_input.send_keys("4242")
        card_number_input.send_keys("4242")
        card_number_input.send_keys("4242")
        card_exp_input.send_keys("12")
        card_exp_input.send_keys("17")
        card_cvc_input.send_keys("123")
        pay_button.click()
        self.browser.implicitly_wait(10)
 
        # The stripe payment overlay goes away and she returns to course page

        # Now, the Enrol button is gone.
        #with self.assertRaises(NoSuchElementException):
        #    enrol = self.browser.find_element_by_id('id_enrol_button')
    
        # And, she can access all the lessons.
        lesson2_url = "{0}/courses/1/lesson/2/".format(self.server_url)
        second_lesson = self.browser.find_element_by_id('id_lesson2')
        second_lesson.click()
        self.assertEqual(self.browser.current_url,  lesson2_url)

        # Logging out and later, logging in again, her course access is still
        # available.
        self._logUserOut()
        self._logUserIn('helmi', 'plate509')
        self.browser.get(lesson2_url)

        # On her profile page, she can see which courses she has paid for, 
        # along with how much was paid and when.
        self.browser.get('{0}/accounts/profile/'.format(self.server_url))
        receipts_area = self.browser.find_element_by_id('id_receipts')
        course_receipt = receipts_area.find_element_by_id('id_receipt_1')

    def test_author_reviews_paid_enrolments_for_course(self):
        # Gordon has been organiser/instructor for a couple of courses
        # On his profile page he can see the two courses he's involved with.
        # Selecting one, he is taken to a page summarising his students' 
        # interactions on that course.
        # He can see the total number of enrolments
        # There is a section detailing total lesson views
        # And a list of enrolment payments made, along with date made.
        self.fail("Write now")
