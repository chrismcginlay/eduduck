from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest

from courses.forms import (
    ABSTRACT_FIELD_REQUIRED_ERROR,
    CODE_FIELD_REQUIRED_ERROR,
    NAME_FIELD_REQUIRED_ERROR,
)

class RegisteredUserInteractsWithCourse(FunctionalTest):

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

        
class AuthorCreatesMaterials(FunctionalTest):

    def test_can_create_course_and_retrieve_it_later(self):
        # Urvasi visits the site and immediately decides to create a course
        self.browser.get(self.server_url)

        # There is a text-box inviting her to create a new course.
        text_box = self.browser.find_element_by_xpath(
            "//input[@id='id_course_name']")
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        
        # She tries to create a course on Origami
        text_box.send_keys('Origami')
        create.click()
        
        # Since she has not logged in, she is invited to do so:
        redirect_url = '/accounts/login/?next=/courses/create/'
        self.assertIn(redirect_url, self.browser.current_url)
        
        # Urvasi logs in to the site...
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')

        # ...and then returns to the homepage.
        self.browser.get(self.server_url)
        
        # There is a text-box inviting her to create a new course.
        text_box = self.browser.find_element_by_xpath(
            "//input[@id='id_course_name']")
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        
        # She begins by trying to create a course called
        # 'The Art and Craft of Camping in a UK Summer'
        text_box.send_keys('The Art and Craft of Camping in a UK Summer')
        create.click()
        
        # This is forwarded to a course create form with additional fields.
        self.assertRegexpMatches(self.browser.current_url, '/courses/create/')
        course_name_box = self.browser.find_element_by_xpath(
            "//input[@id='id_name']")
        self.assertEqual(course_name_box.get_attribute('value'),
                         'The Art and Craft of Camping in a UK Summer')
        self.assertIn('id_abstract', self.browser.page_source)
        self.assertIn('id_code', self.browser.page_source)
        
        # She tries to create the course, but has not given a code or abstract
        # Also the course name is rejected as being too long
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        create.click()
        too_long_err = "Ensure this value has at most 20 characters"
        self.assertIn(too_long_err, self.browser.page_source)
        self.assertIn(CODE_FIELD_REQUIRED_ERROR, self.browser.page_source)
        self.assertIn(ABSTRACT_FIELD_REQUIRED_ERROR, self.browser.page_source)
        
        # She renames her new course 'Camping'...
        text_box = self.browser.find_element_by_xpath(
            "//input[@id='id_name']")
        text_box.clear()
        text_box.send_keys('Camping')
        
        # On completing and submitting the form, the course is created in the
        # database, she is then taken to a new URL with all the fields
        # re-presented to her. 
        code_box = self.browser.find_element_by_xpath(
            "//input[@id='id_code']")
        abstract_box = self.browser.find_element_by_xpath(
            "//textarea[@id='id_abstract']")
        code_box.send_keys('CAMP01')
        abstract_box.send_keys('Being organised is the key to a happy camp')
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        create.click()
        target_url = self.server_url + '/courses/\d+/'
        self.assertRegexpMatches(self.browser.current_url, target_url)

        # She notices that there is an 'edit' button on this course page
        btn_edit = self.browser.find_element_by_id('id_course_edit')
        btn_submit = self.browser.find_element_by_id('id_submit')
        # She decides to improve the abstract:
        btn_edit.click()
        target_url = self.server_url + '/courses/1/edit/'
        self.assertEqual(target_url, self.browser.current_url)
        self.assertIn('<h2>Edit Course</h2>', self.browser.page_source)
        abstract_box = self.browser.find_element_by_id('id_abstract')
        abstract_box.send_keys(". Wibble.")
        btn_submit.click()
        
        target_url = self.server_url + '/courses/1/'
        self.assertEqual(target_url, self.browser.current_url)
        
        # Before Urvasi has time to add lessons, she has to go out, so logs out.
        self._logUserOut()
        
        # Later she returns to the site, logs in and immediately sees her new
        # course listed in her profile area. Happy days.
        self._logUserIn('urvasi', 'hotel23')
        self.fail('Not implemented yet')
        
        # On the homepage, there is still a textbox for adding another course. 
        # She adds a course on 'Mountain Leadership'.
        
        # She returns to the profile page, where now both courses are listed.
        # Now a new user, Albert, comes along to the site
        self.browser.quit()

        ## Clean browser instance - no cookie data etc.
        self.browser = webdriver.Firefox()

        # Albert visits the homepage. He sees both of Urvasi' courses under
        # 'available courses' but cannot edit them.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Camping', page_text)
        self.assertIn('Mountain Leadership', page_text)
        self.fail("test cannot edit them")

        # Albert now logs in and again sees both courses under 'available'
        # in his profile area. He enrols in 'Camping' and is taken to a new URL

        # This shows a list of lessons in the Camping course (currently zero)

        # He returns to his profile area and is pleased to see the Camping
        # course listed under 'Your Courses' and the first aid one still under
        # 'available'

    def test_can_delete_course(self):
        self.fail("write")

    @skip("")
    def test_can_create_and_retrieve_lessons_associated_with_course(self):
        self.fail("Write test")

    @skip("")
    def test_can_populate_course_with_resources(self):
        """Author is able to create attachments, videos, LOs etc for course"""

        self.fail("Write test")

    @skip("")
    def test_can_edit_lesson_populating_with_resources(self):
        """Author can create attachments, videos, LOs etc for lesson"""

        self.fail("Write test")