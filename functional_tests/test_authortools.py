from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest

from courses.forms import (
    ABSTRACT_FIELD_REQUIRED_ERROR,
    NAME_FIELD_REQUIRED_ERROR,
)

class AuthorUsesCourseAuthoringTools(FunctionalTest):
    
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
        
        # She tries to create the course, but has not given an abstract
        # Also the course name is rejected as being too long
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        create.click()
        too_long_err = "Ensure this value has at most 20 characters"
        self.assertIn(too_long_err, self.browser.page_source)
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
        btn_edit = self.browser.find_element_by_id('id_edit_course')
        edit_target_url = self.server_url + '/courses/\d+/edit/'
        # She decides to improve the abstract:
        btn_edit.click()
        self.assertRegexpMatches(self.browser.current_url, edit_target_url)
        self.assertIn('<h2 id="id_page_title">Edit Course</h2>', self.browser.page_source)
        abstract_box = self.browser.find_element_by_id('id_abstract')
        abstract_box.send_keys(". Wibble.")
        # and delete the course code
        code_box = self.browser.find_element_by_xpath("//input[@id='id_code']")
        code_box.clear()
        # she submits the changes
        btn_submit = self.browser.find_element_by_id('id_submit_edits')
        btn_submit.click()
        
        target_url = self.server_url + '/courses/\d+/'
        self.assertRegexpMatches(self.browser.current_url, target_url)
        
        # Before Urvasi has time to add lessons, she has to go out, so logs out.
        self._logUserOut()
        
        # Later she returns to the site, logs in and immediately sees her new
        # course listed in correct part of profile area. Happy days.
        self._logUserIn('urvasi', 'hotel23')
        coursearea = self.browser.find_element_by_id('id_courses_taught')
        self.assertIn('Camping', coursearea.text)
        
        # Now a new user, Albert, comes along to the site
        self.browser.quit()
        
        ## Clean browser instance - no cookie data etc.
        self.browser = webdriver.Firefox()
        
        # Albert visits the course index. He sees Urvasi's course, visits its page
        self.browser.get(self.server_url+'/courses/')
        courses_area = self.browser.find_element_by_id('id_course_selection') 
        target_course = self.browser.find_element_by_id('id_Camping_course')
        target_course.click()
        title = self.browser.find_element_by_id('id_course_title')
        self.assertIn('Camping', title.text) 
        
    def test_can_delete_course(self):
        self.fail("not implemented")
        
class AuthorCreatesAndEditsLessons(FunctionalTest):

    def test_can_create_retrieve_edit_lessons_associated_with_course(self):
	""" Starting from an existing course page """
	
        self.browser.get(self.server_url)
	self._logUserIn('chris', 'chris')
	self.browser.get(self.server_url+'/courses/1')
        # Chris sees the edit course button and clicks it
	btn_edit = self.browser.find_element_by_id('id_edit_course')
	lesson_set_target_url = self.server_url + '/courses/1/edit'
        btn_edit.click()
	self.assertRegexpMatches(self.browser.current_url, lesson_set_target_url)

	# On the edit page, there is a section noting the name of 
	# course followed by a section listing the existing lessons by title 
        pt = self.browser.find_element_by_id('id_page_title')
	self.assertIn('Blender', pt.text)
	lessons_area = self.browser.find_element_by_id('id_lesson_formset_area') 

	f0 = self.browser.find_element_by_xpath("//input[@name='lesson_formset-0-name']")
	f1 = self.browser.find_element_by_xpath("//input[@name='lesson_formset-1-name']")
	f2 = self.browser.find_element_by_xpath("//input[@name='lesson_formset-2-name']")
	self.assertEqual('What is Blender for?', f0.get_attribute('value'))
	self.assertEqual('Basics of the User Interface', f1.get_attribute('value'))
	self.assertEqual('Orientation in 3D Space', f2.get_attribute('value'))	
	
	# And an area for the purpose of adding more lessons, containing a text box 
	# for a lesson title, another for an abstract.
	new_lesson_name = self.browser.find_element_by_xpath(
	    "//input[@name='lesson_formset-3-name']")
	new_lesson_abstract = self.browser.find_element_by_xpath(
	    "//textarea[@name='lesson_formset-3-abstract']")

	# Chris decides to add a lesson called 'Materials'
	# with a suitable abstract.
	new_lesson_name.send_keys('Materials')
	new_lesson_abstract.send_keys('How to create, use share and delete materials')

	# He can edit any of the titles and abstracts of the lessons,
	# with the updates saved on hitting submit as before.
	lesson2_name = self.browser.find_element_by_xpath(
	    "//input[@name='lesson_formset-2-name']")
	lesson2_name.send_keys('Test')
	lesson2_abstract = self.browser.find_element_by_xpath(
	    "//textarea[@name='lesson_formset-2-abstract']")
	# On submitting this the course page reloads with his lesson alterations.
	submit_edits_button = self.browser.find_element_by_id('id_submit_edits2')
	submit_edits_button.click()
	
	paginator = self.browser.find_element_by_class_name('pure-paginator')
	self.assertEqual(len(paginator.find_elements_by_tag_name('li')), 4)
	self.assertIn('Materials', self.browser.page_source)
	self.assertIn('How to create, use share and delete materials', self.browser.page_source)
                  
    @skip("")
    def test_can_populate_course_with_resources(self):
        """Author is able to create attachments, videos, LOs etc for course"""
        
        self.fail("Write test")
    
    @skip("")
    def test_can_populate_lesson_with_resources(self):
        """Author can create attachments, videos, LOs etc for lesson"""
        
        self.fail("Write test")
