#functional_tests/test_authortools.py
import os
import requests
from django.core.files.uploadedfile import TemporaryUploadedFile
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from unittest import skip
from urllib import unquote

from .base import FunctionalTest

from courses.forms import (
    COURSE_ABSTRACT_FIELD_REQUIRED_ERROR,
    COURSE_NAME_FIELD_REQUIRED_ERROR,
)
from video.utils import VIDEO_URL_FIELD_INVALID_ERROR

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
        course_finish_url = '/courses/create/%3Fcourse_short_name%3DOrigami'
        redirect_url = '/accounts/login/?next='+course_finish_url
        self.assertIn(redirect_url, self.browser.current_url)
        
        # Urvasi logs in to the site...
        self._logUserIn('urvasi', 'hotel23', 
            next_url=course_finish_url)
        
        # ...and is redirected to complete the course creation process.
        target_url = self.server_url + unquote(course_finish_url)
        self.assertEqual(self.browser.current_url, target_url)
        
        # Her Origami course title is there
        course_name_box = self.browser.find_element_by_xpath(
            "//input[@id='id_name']")
        self.assertEqual(course_name_box.get_attribute('value'),
                         'Origami')
        self.assertIn('id_abstract', self.browser.page_source)
        self.assertIn('id_code', self.browser.page_source)
        # For some reason she decides to change from Origami to Camping:
        course_name_box.clear()
        course_name_box.send_keys('The Art and Craft of Camping')

        # She tries to create the course, but has not given an abstract
        # Also the course name is truncated at 20 characters
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        create.click()
        course_name_box = self.browser.find_element_by_xpath(
            "//input[@id='id_name']")
        self.assertEqual(
            course_name_box.get_attribute('value'), 'The Art and Craft of')
        self.assertIn(COURSE_ABSTRACT_FIELD_REQUIRED_ERROR,
            self.browser.page_source)
        
        # She renames her new course 'Camping'...
        course_name_box = self.browser.find_element_by_xpath(
            "//input[@id='id_name']")
        course_name_box.clear()
        course_name_box.send_keys('Camping')
        
        # She completes and submits the form
        code_box = self.browser.find_element_by_xpath(
            "//input[@id='id_code']")
        abstract_box = self.browser.find_element_by_xpath(
            "//textarea[@id='id_abstract']")
        code_box.send_keys('CAMP01')
        # There is a a message indicating Markdown can be used on abstracts
        info = self.browser.find_element_by_xpath(
            "//label[@for='id_abstract']/following-sibling::"\
            "div[@class='markdown']/p[@class='markdown']")
        self.assertEqual(info.text, 'Use Markdown!')

        # So, she uses some markdown on the abstract
        abstract_box.send_keys('Being *organised* is the key to a happy camp')
        create = self.browser.find_element_by_xpath(
            "//button[@id='id_course_create']")
        create.click()

        # The course is created in the database, 
        # she is then taken to a new URL with all the fields 
        # re-presented to her. 
        target_url = self.server_url + '/courses/\d+/'
        self.assertRegexpMatches(self.browser.current_url, target_url)
        abstract_box =  self.browser.find_element_by_xpath(
            "//div[@id='id_abstract']/p[3]")
        # The abstract correctly displays markdown
        self.assertEqual(
            abstract_box.get_attribute('innerHTML'), 
            u'Being <em>organised</em> is the key to a happy camp'
        )

        # The course is by default 'unpublished' and thus a 'publish' button
        # is visible
        publish_button = self.browser.find_element_by_id('id_publish_button')
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_published_message')
 
        # She notices that there is an 'edit' button on this course page
        btn_edit = self.browser.find_element_by_id('id_edit_course')
        edit_target_url = self.server_url + '/courses/\d+/edit/'
        
        # She decides to improve the abstract, so edits the page:
        btn_edit.click()
        self.assertRegexpMatches(self.browser.current_url, edit_target_url)
        self.assertIn('<h2 id="id_page_title">Editing: Camping</h2>', 
            self.browser.page_source)

        # There is a message indicating Markdown can be used on abstracts
        info = self.browser.find_element_by_xpath(
            "//p[@class='markdown']")
        self.assertEqual(info.text, 'Use Markdown!')

        # ...and makes the edit...
        abstract_box = self.browser.find_element_by_id('id_course_form-abstract')
        abstract_box.send_keys(". Wibble.")
        # ...and delete the course code
        code_box = self.browser.find_element_by_xpath(
            "//input[@id='id_course_form-code']")
        code_box.clear()
        # she submits the changes
        btn_submit = self.browser.find_element_by_id('id_submit_course_edits')
        btn_submit.click()
        
        target_url = self.server_url + '/courses/\d+/'
        self.assertRegexpMatches(self.browser.current_url, target_url)
       
        # Urvasi knows that there is a course enrol page and quickly
        # checks that the markdown is rendered in the abstracts
        enrol_url = self.browser.current_url + 'enrol/'
        self.browser.get(enrol_url)
        abstract_box =  self.browser.find_element_by_xpath(
            "//div[@id='id_abstract']/p[3]")
        # The abstract correctly displays markdown as before
        self.assertEqual(
            abstract_box.get_attribute('innerHTML'), 
            u'Being <em>organised</em> is the key to a happy camp. Wibble.'
        )

        # Before Urvasi has time to add lessons, she has to go out, so logs out.
        self._logUserOut()
        
        # Later she returns to the site, logs in and immediately sees her new
        # course listed in correct part of profile area. Happy days.
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')
        coursearea = self.browser.find_element_by_id('id_courses_taught')
        self.assertIn('Camping', coursearea.text)
        
        # Now a new user, Albert, comes along to the site
        self.browser.quit()
        
        ## Clean browser instance - no cookie data etc.
        self.browser = webdriver.Firefox()

        # Albert visits the course index, but Urvasi's course isn't there 
        # because she hasn't published it yet.
        self.browser.get(self.server_url+'/courses/')
        courses_area = self.browser.find_element_by_id('id_course_selection') 
        with self.assertRaises(NoSuchElementException): 
            self.browser.find_element_by_id('id_Camping_course')

        # So Urvasi then publishes the course
        self.browser.get(self.server_url)
        self._logUserIn('urvasi', 'hotel23')
        self.browser.get(self.server_url+'/courses/')
        target_course = self.browser.find_element_by_id('id_Camping_course')
        target_course.click()
        course_url = self.browser.current_url
        publish_confirmation_url = "{0}publish/".format(course_url)
        publish_button = self.browser.find_element_by_id('id_publish_button')
        publish_button.click()
       
        self.assertEqual(self.browser.current_url, publish_confirmation_url)
        publish_button = self.browser.find_element_by_id('id_course_publish')
        publish_button.click()
        self.assertEqual(self.browser.current_url, publish_confirmation_url)
        self.browser.find_element_by_id('id_course_link').click()
        self.assertEqual(self.browser.current_url, course_url)
 
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('id_publish_button')
        self.browser.find_element_by_id('id_published_message')

        # Albert visits the course index. He sees Urvasi's course, visits its page
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.server_url+'/courses/')
        courses_area = self.browser.find_element_by_id('id_course_selection') 
        target_course = self.browser.find_element_by_id('id_Camping_course')
        target_course.click()
        self.browser.implicitly_wait(10)
        title = self.browser.find_element_by_id('id_course_title')
        self.assertIn('Camping', title.text) 
        
    def test_can_delete_course(self):
        self.fail("not implemented course delete yet")
 
    def test_can_populate_course_with_video_resources(self):
        # sven wants to have a nice intro video on course 3
        # embedded on the course home page. He goes to the edit page
        self.browser.get(self.server_url)
        self._logUserIn('sven', 'sven')
        self.browser.get(self.server_url+'/courses/3/edit/')

        # he sees an area on the course form for adding a youtube intro video.
        vfs = self.browser.find_element_by_id('id_video_formset_area')
        video_name_widget = vfs.find_element_by_name('video_formset-0-name')
        video_url_widget = vfs.find_element_by_id('id_video_formset-0-url')

        # sven thinks that he has the desired url in clipboard and pastes 
        # but unfortunately the clipboard just pastes garbage which he submits
        self._expand_all_collapsible_blocks()
        video_name_widget.send_keys("My Intro Video")
        video_url_widget.send_keys("httttp://yotub.com/notvalid")
        btn_submit = vfs.find_element_by_id('id_submit_video_edits')
        btn_submit.click()

        self._expand_all_collapsible_blocks()
        # The invalid url is picked up and an error message is displayed.
        self.assertIn(VIDEO_URL_FIELD_INVALID_ERROR, self.browser.page_source)
        # sven now puts in the correct url and resubmits.
        vfs = self.browser.find_element_by_id('id_video_formset_area')
        video_name_widget = vfs.find_element_by_name('video_formset-0-name')
        video_name_widget.clear()
        self._expand_all_collapsible_blocks()
        video_name_widget.send_keys("My Intro Video")
        video_url_widget = vfs.find_element_by_id('id_video_formset-0-url')
        video_url_widget.clear()
        video_url_widget.send_keys("http://www.youtube.com/embed/uIlu7szab5I")
        btn_submit = vfs.find_element_by_id('id_submit_video_edits')
        btn_submit.click()
        # All is well, the video shows up on the course homepage.
        self.assertEqual(self.browser.current_url, self.server_url+'/courses/3/')
        vid = self.browser.find_element_by_id('id_intro_video')
        self.assertIn('My Intro Video', vid.text)

        # Finally he decides to delete introductory video entirely.
        self.browser.get(self.server_url+'/courses/3/edit/')
        delete_check = self.browser.find_element_by_id('id_video_formset-0-DELETE')
        delete_check.click()
        btn_submit = self.browser.find_element_by_id('id_submit_video_edits')
        btn_submit.click()
 
        # It no longer appears on the course page.
        self.browser.get(self.server_url+'/courses/3/')
        self.assertNotIn('My Intro Video', self.browser.page_source)
       
    def test_can_populate_course_with_attachments(self):
        # Helen now wishes to add some attachments to the course 4 page.
        self.browser.get(self.server_url)
        self._logUserIn('helen', 'helen')
        self.browser.get(self.server_url+'/courses/4/edit/')

        # On the edit page she sees an area for adding attachments.
        afs = self.browser.find_element_by_id('id_attachment_formset_area')
        attachment_name_widget = afs.find_element_by_name(
            'attachment_formset-0-name')
        attachment_file_widget = afs.find_element_by_name(
            'attachment_formset-0-attachment')
        attachment_desc_widget = afs.find_element_by_id(
            'id_attachment_formset-0-desc')

        # There is a message indicating Markdown can be used on descriptions 
        info = afs.find_element_by_xpath(
            "descendant::div[@class='markdown']/p[@class='markdown']")
        self.assertEqual(info.text, 'Use Markdown!')
        
        # She uploads a course intro (maybe a PDF).
        with TemporaryUploadedFile('atest.txt', 'text/plain', None, None) as fp:
            fp.write("Write some bytes")
            fp.flush()
            attachment_file_widget.send_keys(fp.temporary_file_path())
            attachment_name_widget.send_keys("A test file")
            attachment_desc_widget.send_keys("A **test** description")
            btn=self.browser.find_element_by_id('id_submit_attachment_edits')
            btn.click()
        
        attachment_desc =  self.browser.find_element_by_xpath(
            "//div[@id='id_resource_attachments']")
        # The abstract correctly displays markdown
        self.assertIn(
            u'A <strong>test</strong> description',
            attachment_desc.get_attribute('outerHTML'), 
        )
        
        # This is scanned for virus payload, clear.
        # self.fail("Scan attachments for viruses at commented line above")

        # The course page reloads, showing the attachment
        url = self.browser.current_url
        self.assertEqual(url, self.server_url+'/courses/4/')
        attachment_list = self.browser.find_element_by_id('id_attachment_list')
        first_attachment = attachment_list.find_element_by_tag_name('a')
        self.assertEqual('A test file', first_attachment.text)

        # Helen is able to download the attachment, just 'cos she wants to.
        # get the sessionid from the Selenium browser session and borrow it for
        # log in via requests.
        cookies = self.browser.get_cookies() 
        ssid = filter(lambda cookie: cookie['name'] == 'sessionid', cookies)[0]['value']
        s = requests.Session()
        response = s.head(
            first_attachment.get_attribute('href'),
            allow_redirects=True,
            cookies={'sessionid':ssid}
        )

        #should redirect to download resource
        self.assertEqual(response.history[0].status_code, 302)
        self.assertIn(
            'interaction/attachment/10/download/',
            response.history[0].url
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '/media/attachments/',
            response.url
        )

        # Helen then revisits the edit page, uploads a second attachment.
        self.browser.get(self.server_url+'/courses/4/edit/')
        afs = self.browser.find_element_by_id('id_attachment_formset_area')
        attachment_name_widget = afs.find_element_by_name(
            'attachment_formset-1-name')
        attachment_file_widget = afs.find_element_by_name(
            'attachment_formset-1-attachment')
        attachment_desc_widget = afs.find_element_by_id(
            'id_attachment_formset-1-desc')
        with TemporaryUploadedFile('atest2.txt', 'text.plain', None, None) as fp2:
            fp2.write("Write some bytes")
            fp2.flush()
            attachment_file_widget.send_keys(fp2.temporary_file_path())
            attachment_name_widget.send_keys("Another test file")
            btn=self.browser.find_element_by_id('id_submit_attachment_edits')
            btn.click()

        # This is visible on the course page
        self.assertIn('Another test file', self.browser.page_source)

        # Helen finally decides to delete the course intro attachment.
        self.browser.get(self.server_url+'/courses/4/edit/')
        delete_check = self.browser.find_element_by_id('id_attachment_formset-0-DELETE')
        delete_check.click()
        btn_submit = self.browser.find_element_by_id('id_submit_attachment_edits')
        btn_submit.click()
 
        # It no longer shows up on the course page but the second attachment 
        # is still there.
        self.browser.get(self.server_url+'/courses/4/')
        self.assertIn('Another test file', self.browser.page_source)
        self.assertNotIn('A test file', self.browser.page_source)

        self.fail("Scan attachments for viruses at commented line above")

        
class AuthorCreatesAndEditsLessons(FunctionalTest):

    def test_can_create_retrieve_edit_lessons_associated_with_course(self):
        """ Starting from an existing course page """
    
        self.browser.get(self.server_url)
        self._logUserIn('sven', 'sven')
        self.browser.get(self.server_url+'/courses/1')
        # sven sees the edit course button and clicks it
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

        self._expand_all_collapsible_blocks() 

        # sven decides to add a lesson called 'Materials'
        # with a suitable abstract.
        new_lesson_name.send_keys('Materials')
        new_lesson_abstract.send_keys('How to create, use share and delete materials')
        # There is a message indicating Markdown can be used on abstracts
        info = lessons_area.find_element_by_xpath(
            "descendant::div[@class='markdown']/p[@class='markdown']")
        self.assertEqual(info.text, 'Use Markdown!')

        # He can edit any of the titles and abstracts of the lessons,
        # with the updates saved on hitting submit as before.
        lesson2_name = self.browser.find_element_by_xpath(
            "//input[@name='lesson_formset-2-name']")
        lesson2_name.send_keys('Test')
        lesson2_abstract = self.browser.find_element_by_xpath(
            "//textarea[@name='lesson_formset-2-abstract']")
        # On submitting this the course page reloads with his lesson alterations.
        submit_edits_button = self.browser.find_element_by_id('id_submit_lesson_edits')
        submit_edits_button.click()
        
        paginator = self.browser.find_element_by_class_name('pure-paginator')
        self.assertEqual(len(paginator.find_elements_by_tag_name('li')), 4)
        self.assertIn('Materials', self.browser.page_source)
        self.assertIn('How to create, use share and delete materials', 
            self.browser.page_source)
                  
    def test_lesson_renders_markdown_in_abstract(self):
        """Markdown used in lesson abstract is rendered"""

        # sven logs in and heads to the first course page.
        self.browser.get(self.server_url)
        self._logUserIn('sven', 'sven')
        self.browser.get(self.server_url+'/courses/1/lesson/1/edit/')

        self._expand_all_collapsible_blocks()
        basics_area = self.browser.find_element_by_id(
            'id_lesson_basics_area')
        abstract_text_box = self.browser.find_element_by_id(
            'id_lesson_form-abstract')
        abstract_text_box.send_keys("Some *bold* markdown")
        
        btn_submit = self.browser.find_element_by_id('id_submit_lesson_edits')
        btn_submit.click()

        #The markdown is rendered to HTML
        self.assertIn("Some <em>bold</em> markdown", self.browser.page_source)

    def test_can_populate_lesson_with_videos(self):
        """Author can create videos for lesson"""
    
        # Sven logs in and heads to the first course page.
        self.browser.get(self.server_url)
        self._logUserIn('sven', 'sven')
        self.browser.get(self.server_url+'/courses/1/')

        # He visits a lesson page,
        self.browser.find_element_by_id('id_lesson1').click()
        
        # There he sees a lesson edit button, clicks it...
        btn_edit = self.browser.find_element_by_id('id_edit_lesson')
        lesson_set_target_url = self.server_url + '/courses/1/lesson/1/edit/'
        btn_edit.click()
        self.assertRegexpMatches(self.browser.current_url, lesson_set_target_url)

        # The lesson edit page is split into logical sections
        pt = self.browser.find_element_by_id('id_page_title')
        self.assertIn('What is Blender for?', pt.text)
        basics_area = self.browser.find_element_by_id(
            'id_lesson_basics_area')
        video_area = self.browser.find_element_by_id(
            'id_video_formset_area')
        attachments_area = self.browser.find_element_by_id(
            'id_attachment_formset_area')
        learning_intention_area = self.browser.find_element_by_id(
            'id_learning_intention_formset_area')

        # sven tries to add a video to the lesson page, 
        # but he enters a duff url.
        self._expand_all_collapsible_blocks()
        video_name_widget = self.browser.find_element_by_xpath(
            "//input[@name='video_formset-0-name']")
        video_url_widget = self.browser.find_element_by_xpath(
            "//input[@name='video_formset-0-url']")
        video_name_widget.clear()
        video_url_widget.clear()
        video_name_widget.send_keys("Broken url")
        video_url_widget.send_keys("https://www.youtube.com/watch?v=kT")
        btn_submit = self.browser.find_element_by_id('id_submit_video_edits')
        btn_submit.click()
        
        # This triggers an error message
        self.assertIn(VIDEO_URL_FIELD_INVALID_ERROR, self.browser.page_source)

        # On fixing the error, the edits save properly and the video is embedded
        self._expand_all_collapsible_blocks()
        video_url_widget = self.browser.find_element_by_xpath(
            "//input[@name='video_formset-0-url']")
        video_url_widget.clear()
        video_url_widget.send_keys(
            "https://www.youtube.com/watch?v=kT7qrYi8R_M")
        btn_submit = self.browser.find_element_by_id('id_submit_video_edits')
        btn_submit.click()
        
        self.assertEqual(
            self.browser.current_url, self.server_url+'/courses/1/lesson/1/')
        vid = self.browser.find_element_by_id('id_video_1')

        # sven logs out and finds that the resources are of course still available
        # to casual site visitors.
        self._logUserOut()
        self.browser.get(self.server_url+'/courses/1/lesson/1/')
        self.browser.find_element_by_id('id_video_1') 

    def test_author_can_populate_lesson_with_attachments(self):
        # sven now wishes to add some attachments to course 1 lesson 3.
        # On the edit page he sees an area for adding attachments.
        self.browser.get(self.server_url)
        self._logUserIn('sven', 'sven')
        self.browser.get(self.server_url+'/courses/1/lesson/3/edit/')
        afs = self.browser.find_element_by_id('id_attachment_formset_area')
        
        # There are suitable fields for a name and description of the file
        attachment_name_widget = afs.find_element_by_name(
            'attachment_formset-0-name')
        attachment_file_widget = afs.find_element_by_name(
            'attachment_formset-0-attachment')
        attachment_desc_widget = afs.find_element_by_name(
            'attachment_formset-0-desc')
        afs.find_element_by_id('id_attachment_formset-0-desc')

        # There is a message indicating Markdown can be used on descriptions 
        info = afs.find_element_by_xpath(
            "descendant::div[@class='markdown']/p[@class='markdown']")
        self.assertEqual(info.text, 'Use Markdown!')

        # He uploads a lesson summary (maybe a PDF).
        with TemporaryUploadedFile('atest.txt', 'text/plain', None, None) as fp:
            fp.write("Write some bytes")
            fp.flush()
            attachment_file_widget.send_keys(fp.temporary_file_path())
            attachment_name_widget.send_keys("A test file")
            attachment_desc_widget.send_keys("A **test** description")
            btn=self.browser.find_element_by_id('id_submit_attachment_edits')
            btn.click()
        
        attachment_desc =  self.browser.find_element_by_xpath(
            "//div[@id='id_resource_attachments']")
        # The abstract correctly displays markdown
        self.assertIn(
            u'A <strong>test</strong> description',
            attachment_desc.get_attribute('outerHTML'), 
        )

        # This is scanned for virus payload, clear.
        #TODO scan
        
        # Having saved the edits, the lesson page reloads, showing the attachment
        # This downloads successfully.
        
        url = self.browser.current_url
        self.assertEqual(url, self.server_url+'/courses/1/lesson/3/')
        attachment_list = self.browser.find_element_by_id('id_attachment_list')
        first_attachment = attachment_list.find_element_by_tag_name('a')
        self.assertIn('A test file', first_attachment.text)

        # Helen is able to download the attachment, just 'cos she wants to.
        response = requests.head(first_attachment.get_attribute('href'))
        self.assertEqual(response.status_code, 302)
        attachment_list = self.browser.find_element_by_id('id_attachment_list')
        first_attachment = attachment_list.find_element_by_tag_name('a')
        self.assertIn('A test file', first_attachment.text)

        self.fail("Write the virus payload scan test referred above")

    def test_author_can_populate_lesson_with_outcomes_etc(self):
        # Sven wants to set up a few learning intentions (aka key areas) 
        # and associated specific learning outcomes (aka capacities, facts)
        # and success criteria (aka assessable activities).

        # There is an area on the lesson edit page for LIs.
        self.browser.get(self.server_url)
        self._logUserIn('sven', 'sven')
        self.browser.get(self.server_url+'/courses/1/lesson/3/edit/')
        lifs = self.browser.find_element_by_id(
            'id_learning_intention_formset_area')

        # There are text areas for adding learning intentions 
        li_text0_widget = lifs.find_element_by_name(
            'learning_intention_formset-0-text')
        li_text1_widget = lifs.find_element_by_name(
            'learning_intention_formset-1-text')
        # Sven puts in a couple of key areas (learning intentions)
        self._expand_all_collapsible_blocks()
        li_text0_widget.clear()
        li_text1_widget.clear()
        li_text0_widget.send_keys('Learn about average speed')
        li_text1_widget.send_keys('Learn about instantaneous speed')

        btn_submit = self.browser.find_element_by_id(
            'id_submit_learning_intention_edits')
        btn_submit.click()
        # He is able to save the LIs and view the lesson page
        self.assertEqual(
            self.browser.current_url, self.server_url+'/courses/1/lesson/3/')
    
        # Sven's learning intentions are present:
        self.assertIn(
            'Learn about average speed', self.browser.page_source)
        self.assertIn(
            'Learn about instantaneous speed', self.browser.page_source)

        # Sven can navigate to the detail page for each learning intention.
        # From there, he can see associated items about the LI, namely
        # a few success criteria and some learning outcomes.
        LIdetail_link = self.browser.find_element_by_id('id_LI1')
        LIdetail_link.click()
        self.assertEqual(
            self.browser.current_url, self.server_url+'/lesson/3/lint/3/')

        # Since Sven is a course author, he gets an 'Edit' button.
        edit_button = self.browser.find_element_by_id('id_edit_lint')

        # This leads to an edit page where he can edit the main LI itself,
        edit_button.click()
        self.assertEqual(
            self.browser.current_url, self.server_url+'/lesson/3/lint/3/edit/')
        LI_text_input = self.browser.find_element_by_id('id_learning_intention_text')
        LI_text_input.clear()
        LI_text_input.send_keys('Learn how to fry fish')

        # as well as add new or edit existing success criteria or outcomes.
        # (SCs and LOs being organised into two separate areas).
        SCarea = self.browser.find_element_by_id('id_edit_success_criteria')
        LOarea = self.browser.find_element_by_id('id_edit_learning_outcomes')
        SC1_text_input = SCarea.find_element_by_xpath(
            "//input[@name='sc_formset-0-text']")
        SC2_text_input = SCarea.find_element_by_xpath(
            "//input[@name='sc_formset-1-text']")
        LO1_text_input = SCarea.find_element_by_xpath(
            "//input[@name='lo_formset-0-text']")
        LO2_text_input = SCarea.find_element_by_xpath(
            "//input[@name='lo_formset-1-text']") 
        SC1_text_input.send_keys('Test A')
        SC2_text_input.send_keys('Test B')
        LO1_text_input.send_keys('Test C')
        LO2_text_input.send_keys('Test D')

        # There is a button to save edits, which he clicks
        save_button = self.browser.find_element_by_id('id_submit_lilosc_edits')
        save_button.click()

        # This returns him to the learning intention detail page
        self.assertEqual(
            self.browser.current_url, self.server_url+'/lesson/3/lint/3/')

        # where he can see the altered and new SCs and LOs.
        outcomes = self.browser.find_elements_by_class_name('learning_outcome')
        criteria = self.browser.find_elements_by_class_name('criterion')
        self.assertTrue(any('Test A' in criterion.text for criterion in criteria))
        self.assertTrue(any('Test B' in criterion.text for criterion in criteria))
        self.assertTrue(any('Test C' in outcome.text for outcome in outcomes))
        self.assertTrue(any('Test D' in outcome.text for outcome in outcomes))
