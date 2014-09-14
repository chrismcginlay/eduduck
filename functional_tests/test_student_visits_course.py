from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest

class RegisteredUserInteractsWithCourse(FunctionalTest):

    def test_collapsible_blocks_expand_or_collapse(self):
        self.browser.get(self.server_url+'/courses/1/')
        import pdb; pdb.set_trace()
        shadables = self.browser.find_elements_by_class_name('shadable')
        for shadable in shadables:
            shady_bit = shadable.parent().next()
            self.asserTrue(shady_bit.is_displayed())
            shadable.click()
            self.assertFalse(shady_bit.is_displayed())
    
    def test_user_enrols_on_course(self):
        # User Chris logs in.
        self.browser.get(self.server_url)
        self._logUserIn('chris', 'chris')
        
        # he goes back to the homepage
        self.browser.find_element_by_id('id_homelink').click()
        
        # Given that he has not registered on any courses, the homepage shows
        # a selection of courses.
        courses_area = self.browser.find_element_by_id('id_course_selection') 

        # He selects the Fishing course and is taken to that course's homepage
        # where he can view an intro video, see an invitation to enrol
        # see a list of lessons, assessments and resources in the main course
        # resource area

        fishing_course = self.browser.find_element_by_id('id_Line Fishing_course')
        fishing_course.click()
        self.assertTrue(self.browser.find_element_by_id('id_course_title'))
        enrol = self.browser.find_element_by_id('id_enrol_button')
        course_intro = self.browser.find_element_by_id('id_course_intro_area')
        self.assertTrue(course_intro.find_element_by_id('id_abstract'))
        self.assertTrue(course_intro.find_element_by_tag_name('iframe'))
        resource_area = self.browser.find_element_by_id('id_resource_area')
        self.assertTrue(resource_area.find_element_by_id('id_resource_lessons'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_assessments'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_attachments'))
        self.assertTrue(resource_area.find_element_by_id('id_resource_study'))

        # He notices further down the page, that the 'Progress' area offers 
        # yet another opportunity to enrol on the course.
        progress = resource_area.find_element_by_id('id_resource_progress')
        progress.find_element_by_id('id_enrol_button2')
        
        # On enrolling the page reloads and a welcome message appears in the 
        # progress area, instead of the enrol button
        enrol.click()
        resource_area = self.browser.find_element_by_id('id_resource_area')
        progress = resource_area.find_element_by_id('id_resource_progress')
        try:
            progress.find_element_by_id('id_enrol_button2')
        except:
            pass
        self.assertEqual(progress.find_element_by_tag_name('h3').text, "Your Progress")
        
        # Also, on investigating the site menu, he notices that new options
        # are there for the fishing home, lessons, assessments
        menu = self.browser.find_element_by_id('menu')
        items_expected = ['Line Fishing', 'Lessons', 'Assessments',
                          'Intro Videos', 'Study Group', 'Course Docs',
                          'Progress']
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
        
    def test_user_can_complete_or_withdraw_from_course(self):
        self.fail("Write test")
