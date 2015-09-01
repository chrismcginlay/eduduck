#functional_tests/test_paying_for_a_course.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class CanonicalWorkflow(FunctionalTest):

    def test_redirect_unpaid_course_fee_to_payment_mechanism(self):
        # Helmi is visiting the course page for 'Blender' but has not paid
        # The Enrol button shows a course fee
        # She is able to access the first lesson free of charge
        # But the 2nd and later lessons pop up an payment overlay, which she
        # dismisses just now, being redirected to the course homepage.
        # Clicking on Enrol a javascript overlay pops up for Stripe Checkout
        # Helmi pays for the course via Stripe
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
