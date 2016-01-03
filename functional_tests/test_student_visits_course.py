from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from unittest import skip

from .base import FunctionalTest

class LoggedInUserInteractsWithCourse(FunctionalTest):

    class wait_for_element_to_be_invisible(object):
        def __init__(self, element):
            self.element = element
 
        def __call__(self, driver):
            return not(self.element.is_displayed())

    def test_collapsible_blocks_expand_or_collapse(self):
        self.browser.get(self.server_url+'/courses/1/')
        shadables = self.browser.find_elements_by_class_name('shade')
        for shadable in shadables:
            ## parent, then sibling element (*)
            shady_bit = shadable.find_element_by_xpath('../following-sibling::*')
            element = WebDriverWait(self.browser, 10).until(
                EC.visibility_of(shady_bit))
            shadable.click()
            element = WebDriverWait(self.browser, 10).until(
                self.wait_for_element_to_be_invisible(shady_bit))

    def test_user_enrols_on_free_course(self):
        # User Chris logs in.
        self.browser.get(self.server_url)
        self._logUserIn('chris', 'chris')
       
        import pdb; pdb.set_trace() 
        # he goes back to the homepage
        self.browser.find_element_by_id('id_homelink').click()
        
        # and decides to enrol on the line fishing course        
        fishing_course = self.browser.find_element_by_id(
            'id_Line Fishing_course')
        fishing_course.click()
        enrol = self.browser.find_element_by_id('id_enrol_button')
        
        # the course is free so he can enrol without any payment overlay
        self.assertEqual(enrol.text, u'Enrol \xa3Free')
        try:
            progress.find_element_by_class_name('stripe-button-el')
        except NoSuchElementException:
            pass
        enrol.click()

        # the page reloads and the enrol button is replaced with 'enroled'
        self.fail("write me")

    def test_user_enrols_on_course(self):
        # User Chris logs in.
        self.browser.get(self.server_url)
        self._logUserIn('chris', 'chris')
        
        # he goes back to the homepage
        self.browser.find_element_by_id('id_homelink').click()
        
        # Given that he has not enrolled on any courses, the homepage shows
        # a selection of courses.
        courses_area = self.browser.find_element_by_id('id_course_selection') 

        # He selects the Personal Development course and is taken to that 
        # course's homepage where he can view an intro video, see an
        # invitation to enrol see a list of lessons, assessments and resources
        # in the main course resource area

        fishing_course = self.browser.find_element_by_id(
            'id_Personal Development_course')
        fishing_course.click()
        self.assertTrue(self.browser.find_element_by_id('id_course_title'))
        enrol = self.browser.find_element_by_id('id_enrol_button')
    
        # The enrol button includes the price of the course
        self.assertEqual(enrol.text, u'Enrol \xa31.00')
        course_intro = self.browser.find_element_by_id('id_course_intro_area')
        self.assertTrue(course_intro.find_element_by_id('id_abstract'))
        self.assertTrue(course_intro.find_element_by_tag_name('iframe'))
        resource_area = self.browser.find_element_by_id('id_resource_area')
        self.assertTrue(resource_area.find_element_by_id(
            'id_resource_lessons'))
        self.assertTrue(resource_area.find_element_by_id(
            'id_resource_assessments'))
        self.assertTrue(resource_area.find_element_by_id(
            'id_resource_attachments'))
        self.assertTrue(resource_area.find_element_by_id(
            'id_resource_study'))

        # He notices further down the page, that the 'Progress' area offers 
        # yet another opportunity to enrol on the course.
        progress = resource_area.find_element_by_id('id_resource_progress')
        enrol2 = progress.find_element_by_id('id_enrol_button2')

        # This enrol button also includes the price of the course 
        self.assertEqual(enrol2.text, u'Enrol \xa31.00')

        # On enrolling the page reloads and a welcome message appears in the 
        # progress area, instead of the enrol button
        enrol.click()
        resource_area = self.browser.find_element_by_id('id_resource_area')
        progress = resource_area.find_element_by_id('id_resource_progress')
        try:
            progress.find_element_by_id('id_enrol_button2')
        except NoSuchElementException:
            pass
        self.assertEqual(
            progress.find_element_by_tag_name('h3').text, "Your Progress")
        # Also, on investigating the site menu, he notices that new options
        # are there for the Personal Development home, lessons, assessments
        menu = self.browser.find_element_by_id('menu')
        items_expected = [
            'Personal Development', 'Lessons', 'Assessments',
            'Intro Videos', 'Study Group', 'Course Docs',
            'Progress'
        ]
        anchors = menu.find_elements_by_tag_name('a')
        a_list = [a.text for a in anchors]
        for item in items_expected:
            try:
                self.assertTrue(item in a_list)
            except:
                print "{0} not in menu".format(item)
                raise
        
        # On the course homepage, Chris also sees buttons to withdraw from the
        # course or to mark it as 'complete'.
        progress.find_element_by_xpath("//input[@name='course_withdraw']")
        progress.find_element_by_xpath("//input[@name='course_complete']")
    
    def test_author_cannot_enrol_on_own_course(self):
        # User Helen logs in.
        self.browser.get(self.server_url)
        self._logUserIn('helen', 'helen')
        
        # ...goes straight to a course page
        self.browser.get(self.server_url+'/courses/2')
        # We note here that Chris is actually the course organiser
        org = self.browser.find_element_by_xpath(
            "//div[@id='id_abstract']/p[5]")
        self.assertIn("Course organiser Helen", org.text)

        # As such, Helen does NOT see an enrol button.
        try:
            self.browser.find_element_by_id('id_enrol_button')
            self.browser.find_element_by_id('id_enrol_button2')
        except NoSuchElementException:
            pass
        else:
            self.fail("The enrol buttons should NOT be present, but are!")

    def test_instructor_cannot_enrol_on_own_course(self):
        # User Helen logs in.
        self.browser.get(self.server_url)
        self._logUserIn('helen', 'helen')
        
        # ...goes straight to a course page
        self.browser.get(self.server_url+'/courses/2')
        # We note here that Helen is actually the course organiser
        org = self.browser.find_element_by_xpath(
            "//div[@id='id_abstract']/p[6]")
        self.assertIn("Course instructor Helen", org.text)

        # As such, Chris does NOT see an enrol button.
        try:
            self.browser.find_element_by_id('id_enrol_button')
            self.browser.find_element_by_id('id_enrol_button2')
        except NoSuchElementException:
            pass
        else:
            self.fail("The enrol buttons should NOT be present, but are!")   
 
    def test_user_can_complete_or_withdraw_from_course(self):
        self.fail("Write test")
